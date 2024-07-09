import argparse
import subprocess
import os
import tempfile

def run_command(command):
    """Utility function to run a shell command."""
    try:
        result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing {command}: {e.stderr}")
        exit(1)

def run_mq_command(mq_command):
    """Run an MQ command in a shell script with the MQ environment set up."""
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.sh') as script_file:
        script_file.write(f"""
        #!/bin/bash
        . /opt/mqm/bin/setmqenv -s
        {mq_command}
        """)
        script_file_path = script_file.name
    os.chmod(script_file_path, 0o755)
    try:
        output = run_command(f"/bin/bash {script_file_path}")
    finally:
        os.remove(script_file_path)
    return output

def list_queue_managers(args):
    """List all queue managers."""
    output = run_mq_command("dspmq")
    print(output)

def create_queue_manager(args):
    """Create a new queue manager."""
    output = run_mq_command(f"/opt/mqm/bin/crtmqm {args.name} && /opt/mqm/bin/strmqm {args.name}")
    print(f"Queue manager {args.name} created and started.\n{output}")

def create_queue(args):
    """Create a queue in the specified queue manager."""
    mqsc_commands = f"""
    DEFINE QLOCAL('{args.queue_name}') REPLACE
    """
    run_mq_command(f'echo "{mqsc_commands}" | runmqsc {args.qm_name}')
    print(f"Queue {args.queue_name} created in queue manager {args.qm_name}.")

def configure_queue(args):
    """Configure an existing queue in the specified queue manager."""
    mqsc_commands = f"""
    ALTER QLOCAL('{args.queue_name}') {args.configuration}
    """
    run_mq_command(f'echo "{mqsc_commands}" | runmqsc {args.qm_name}')
    print(f"Queue {args.queue_name} configured in queue manager {args.qm_name} with {args.configuration}.")

def start_queue_manager(args):
    """Start a queue manager."""
    output = run_mq_command(f"/opt/mqm/bin/strmqm {args.name}")
    print(f"Queue manager {args.name} started.\n{output}")

def stop_queue_manager(args):
    """Stop a queue manager."""
    output = run_mq_command(f"/opt/mqm/bin/endmqm -i {args.name}")
    print(f"Queue manager {args.name} stopped.\n{output}")

def main():
    parser = argparse.ArgumentParser(description="IBM MQ Management CLI")
    subparsers = parser.add_subparsers(
        title="subcommands", description="valid subcommands", help="additional help"
    )

    # Subparser for listing queue managers
    parser_list = subparsers.add_parser("list_qm", help="List all queue managers")
    parser_list.set_defaults(func=list_queue_managers)

    # Subparser for creating a queue manager
    parser_create_qm = subparsers.add_parser("create_qm", help="Create a new queue manager")
    parser_create_qm.add_argument("name", help="Name of the queue manager to create")
    parser_create_qm.set_defaults(func=create_queue_manager)
    parser_create_qm.epilog = """
    Example usage:
    ibm-mq-cli create_qm QM1
    ibm-mq-cli create_qm MyQueueManager
    """

    # Subparser for creating a queue
    parser_create_queue = subparsers.add_parser("create_queue", help="Create a queue")
    parser_create_queue.add_argument("qm_name", help="Name of the queue manager")
    parser_create_queue.add_argument("queue_name", help="Name of the queue to create")
    parser_create_queue.set_defaults(func=create_queue)
    parser_create_queue.epilog = """
    Example usage:
    ibm-mq-cli create_queue QM1 DEV.QUEUE.1
    ibm-mq-cli create_queue MyQueueManager MyQueue
    """

    # Subparser for configuring a queue
    parser_configure_queue = subparsers.add_parser("configure_queue", help="Configure a queue")
    parser_configure_queue.add_argument("qm_name", help="Name of the queue manager")
    parser_configure_queue.add_argument("queue_name", help="Name of the queue to configure")
    parser_configure_queue.add_argument("configuration", help="Configuration string for the queue")
    parser_configure_queue.set_defaults(func=configure_queue)
    parser_configure_queue.epilog = """
    Example usage:
    ibm-mq-cli configure_queue QM1 DEV.QUEUE.1 "MAXDEPTH(5000)"
    ibm-mq-cli configure_queue MyQueueManager MyQueue "MAXMSGL(104857600)"
    """

    # Subparser for starting a queue manager
    parser_start_qm = subparsers.add_parser("start_qm", help="Start a queue manager")
    parser_start_qm.add_argument("name", help="Name of the queue manager to start")
    parser_start_qm.set_defaults(func=start_queue_manager)
    parser_start_qm.epilog = """
    Example usage:
    ibm-mq-cli start_qm QM1
    ibm-mq-cli start_qm MyQueueManager
    """

    # Subparser for stopping a queue manager
    parser_stop_qm = subparsers.add_parser("stop_qm", help="Stop a queue manager")
    parser_stop_qm.add_argument("name", help="Name of the queue manager to stop")
    parser_stop_qm.set_defaults(func=stop_queue_manager)
    parser_stop_qm.epilog = """
    Example usage:
    ibm-mq-cli stop_qm QM1
    ibm-mq-cli stop_qm MyQueueManager
    """

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()