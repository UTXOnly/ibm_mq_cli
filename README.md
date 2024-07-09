## IBM MQ CLI
IBM MQ CLI is a command-line interface (CLI) tool for managing IBM MQ. It provides functionalities to list queue managers, create queue managers, create queues, and configure queues.

### Features
* List all queue managers
* Create new queue managers
* Create queues in a specified queue manager
* Configure existing queues in a specified queue manager
### Requirements
* IBM MQ must be installed and configured on your system.
    * Strongly reccomend using the [developer install script](https://github.com/ibm-messaging/mq-dev-samples/blob/master/gettingStarted/installing-mq-ubuntu/mq-ubuntu-install.sh)
* Python 3.x must be installed.
* Necessary permissions to execute IBM MQ commands.
### Installation


#### From PyPI
To install from PyPI, run the following command:

```sh
pip install ibm-mq-cli
```

#### From Source
Clone this repository or download the package from PyPI.
Navigate to the project directory.
From Source
To install from the source, run the following commands:

```sh
git clone https://github.com/yourusername/ibm_mq_cli.git
cd ibm_mq_cli
pip install .
```




### Usage
The CLI tool provides the following subcommands:

```
list_qm: List all queue managers.
create_qm: Create a new queue manager.
create_queue: Create a queue in a specified queue manager.
configure_queue: Configure an existing queue in a specified queue manager.
```

#### List All Queue Managers
To list all queue managers, use the following command:

```sh
ibm-mq-cli list_qm
```
#### Create a New Queue Manager
To create a new queue manager, use the following command:

```sh
ibm-mq-cli create_qm <queue_manager_name>
```

##### Example:

```sh
ibm-mq-cli create_qm QM1
```

#### Create a Queue
To create a queue in a specified queue manager, use the following command:

```sh
ibm-mq-cli create_queue <queue_manager_name> <queue_name>
```
##### Example:

```sh
ibm-mq-cli create_queue QM1 DEV.QUEUE.1
ibm-mq-cli create_queue MyQueueManager MyQueue
```
#### Configure a Queue
To configure an existing queue in a specified queue manager, use the following command:

```sh
ibm-mq-cli configure_queue <queue_manager_name> <queue_name> <configuration>
```
##### Example:

```sh
ibm-mq-cli configure_queue QM1 DEV.QUEUE.1 "MAXDEPTH(5000)"
ibm-mq-cli configure_queue MyQueueManager MyQueue "MAXMSGL(104857600)"
```
#### Start Queue Manager
To start a queue manager, use the following command:

```sh
ibm-mq-cli start_qm <queue_manager_name>
```
##### Example:

```sh
ibm-mq-cli start_qm QM1
ibm-mq-cli start_qm MyQueueManager
```

#### Stop Queue Manager
To stop a queue manager, use the following command:
```sh
ibm-mq-cli stop_qm <queue_manager_name>
```
##### Example:
```sh
ibm-mq-cli stop_qm QM1
ibm-mq-cli stop_qm MyQueueManager
```

#### Display Queues
To display all queues in a specified queue manager, use the following command:
```sh
ibm-mq-cli display_queues <queue_manager_name>
```
##### Example:
```sh
ibm-mq-cli display_queues QM1
ibm-mq-cli display_queues MyQueueManager
```

#### Get Queue Permissions
To get permissions for a user on all queues in a specified queue manager, use the following command:
```sh
ibm-mq-cli get_permissions <queue_manager_name> <user>
```
##### Example:
```sh
ibm-mq-cli get_permissions QM1 myuser
ibm-mq-cli get_permissions MyQueueManager anotheruser
```
**Example Output**
```sh
Permissions for queue 'DEV.QUEUE.1':
Entity ubuntu has the following authorizations for object DEV.QUEUE.1:
        get
        browse
        put
        inq
        set
        crt
        dlt
        chg
        dsp
        passid
        passall
        setid
        setall
        clr
```