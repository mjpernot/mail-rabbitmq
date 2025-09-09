# Python project for the processing of emails to be injested into RabbitMQ.
# Classification (U)

# Description:
  Used to process and parse emails that are injested into a queue in RabbitMQ.


###  This README file is broken down into the following sections:
  * Features
  * Prerequisites
  * Installation
  * Configuration
  * Mail Alias Setup
  * Program Help Function
  * Testing
    - Unit
    - Blackbox

# Features:
  * Process and parse emails via mailing pipe.
  * Insert email into correct RabbitMQ queue based on email subject line.
  * Insert email file attachments into correct RabbitMQ queue based on email subject line.

# Prerequisites:

  * Setup a local account and group: rabbitmq:rabbitmq
  * List of Linux packages that need to be installed on the server.
    - python3-pip
    - gcc


# Installation:

Install the program using git 

```
git clone git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/mail-rabbitmq.git
```

Install/upgrade system modules.

NOTE: Install as the user that will run the program.

```
python -m pip install --user -r requirements3.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
```


Install supporting classes and libraries.

```
python -m pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-rabbitmq-lib.txt --target rabbit_lib --trusted-host pypi.appdev.proj.coe.ic.gov
```


# Configuration:

Setup configuration file.
Make the appropriate changes to the RabbitMQ environment in the rabbitmq.py file.
  * Connection information to a RabbitMQ node.
    - user = "USER"
    - japd = "PSWORD"
    - host = "IP_ADDRESS"

  * List of hosts along with their ports to a multiple node RabbitMQ cluster.
    - host_list = []

  * Name of the exchange in the RabbitMQ node.
    - exchange_name = "EXCHANGE_NAME"

  * List of queue names in the RabbitMQ node.
    - valid_queues = ["QueueName1", "QueueName2"]
    - file_queues = ["FileQueueName1", "FileQueueName2"]

  * Name of RabbitMQ queue that will contain any messages/files that do not fit in the other queues (i.e. invalid subject lines).
    - err_queue = "ERROR_QUEUE_NAME"
    - err_file_queue = "ERROR_FILE_QUEUE_NAME"

  * Directory for non-processed emails/log files/temporary storage.
    - email_dir = "DIRECTORY_PATH/email_dir"
    - log_file = "DIRECTORY_PATH/logs/mail_2_rmq.log"
    - tmp_dir = "DIRECTORY_PATH/tmp"

  * Types of attachments to extract from email.
    - attach_types = ["application/pdf", "application/octet-stream"]

  * Dictionary of valid email addresses and their associated queue names.
    - queue_dict = {"name1@domain": "QueueName", "name2@domain": "QueueName2"}

  * Name of error queue to handle incorrect email address or missing attachment.
    - err_addr_queue = "ERROR_ADDR_QUEUE_NAME"

```
cp config/rabbitmq.py.TEMPLATE config/rabbitmq.py
vim config/rabbitmq.py
chmod 600 config/rabbitmq.py
sudo chown rabbitmq:rabbitmq mail-rabbitmq/config/rabbitmq.py
```


# Mail Alias Setup
  * If installing on a postfix system, use the **"Postfix system"** option.  Otherwise use the **"Alias system"** option for all other systems.

### Postfix system

Setup local aliases for rabbitmq account:
  * Run as the rabbitmq user.
  * Add to the .aliases file:
    - `rabbitmq: "|{DIR_PATH}/mail-rabbitmq/mail_2_rmq.py -c rabbitmq -d {DIR_PATH}/mail-rabbitmq/config -M"`

```
vim /home/rabbitmq/.aliases
```

Create aliases database in first term window (run as rabbitmq).
  * Monitor the system messages file for an SELinux policy exceptions, add the exceptions and re-run until no exceptions detected.

```
postalias /home/rabbitmq/.aliases
```

Setup aliases in main.cf file.
  * Add "hash:/home/rabbitmq/.aliases" to the alias_maps and alias_database entries in the main.cf file.  See examples below:
    -  `alias_maps = hash:/home/rabbitmq/.aliases`
    -  `alias_database = hash:/home/rabbitmq/.aliases`

```
sudo vim /etc/postfix/main.cf
```

Reload postfix.
  * Monitor the system messages file for an SELinux policy exceptions, add the exceptions and re-run until no exceptions detected.

```
sudo systemctl restart postfix
```

Send test email to rabbitmq.
  * Monitor the system messages file for an SELinux policy exceptions, add the exceptions and re-run until no exceptions detected.

```
echo "sipr-isse" | mailx -s sipr-isse rabbitmq@mail.domain.name
```


### Alias system
  * This will only work on non-postfix systems.

Add an email alias to allow mail piping.
  * Add the following entry:
    - `mailrabbit: "|{DIR_PATH}/mail_rabbitmq/mail_2_rmq.py -c rabbitmq -d {DIR_PATH}/mail_rabbitmq/config -M"`

```
sudo vim /etc/aliases
sudo newaliases
```

Add links to the program in the /etc/smrsh directory and set ownership.

```
cd /etc/smrsh
sudo ln -s {DIR_PATH}/mail_rabbitmq/mail_2_rmq.py mail_2_rmq.py
sudo chown mail:mail {DIR_PATH}/mail_rabbitmq/config/rabbitmq.py
```


# Program Help Function:

  All of the programs, except the command and class files, will have an -h (Help option) that will show display a help message for that particular program.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:

```
rmq-sysmon/mail_2_rmq.py -h
```


# Testing:

# Unit Testing:

### Installation:

Install the project using the procedures in the Installation section.

### Testing:

```
test/unit/mail_2_rmq/unit_test_run.sh
test/unit/mail_2_rmq/code_coverage.sh
```

# Blackbox Testing:

### Installation:

Install the project using the procedures in the Installation section.

### Configuration:

Create configuration file for testing.
Make the appropriate changes to the RabbitMQ environment in the rabbitmq.py file.
  * "user", "passwd", and "host" is connection information to a RabbitMQ node.
  * "exchange_name" is name of the exchange in the RabbitMQ node.
  * "valid_queues" is a list of queue names in the RabbitMQ node, the queue names are direct correlation to the subject names in the emails.  Note:  Queues names must be PascalCase style.
  * "file_queues" is a list of queue names in the RabbitMQ node, the queue names are direct correlation to the subject names in the emails.  Note:  Queues names must be PascalCase style.
  * "err_queue" is the name of RabbitMQ queue that will contain any messages that do not fit in the other queues (i.e. invalid subject lines).
  * "err_file_queue" is the name of RabbitMQ queue that will contain any file attachments that do not fit in the other queues (i.e. invalid subject lines).
  * "email_dir" is the location where non-processed emails will be saved to (e.g. when RabbitMQ is down).
  * "log_file" is the location of the mail_2_rmq.py log file.
    - user = "USER"
    - passwd = "PASSWORD"
    - host = "HOSTNAME"
    - exchange_name = "EXCHANGE_NAME"
    - valid_queues = ["QUEUE_NAME1", "QUEUE_NAME2"]
    - file_queues = ["FileQueueName1", "FileQueueName2"]
    - err_queue = "ERROR_QUEUE_NAME"
    - err_file_queue = "ERROR_FILE_QUEUE_NAME"
    - email_dir = "DIRECTORY_PATH/email_dir"
    - log_file = "DIRECTORY_PATH/logs/mail_2_rmq.log"

```
cp config/rabbitmq.py.TEMPLATE test/blackbox/mail_2_rmq/config/rabbitmq.py
chmod 600 test/blackbox/mail_2_rmq/config/rabbitmq.py
vim test/blackbox/mail_2_rmq/config/rabbitmq.py
```

Setup a second configuration file to test non-connection logic paths.
  * Change the same variables as listed except change the passwd variable to an incorrect password.

```
cp test/blackbox/mail_2_rmq/config/rabbitmq.py test/blackbox/mail_2_rmq/config/rabbitmq_2.py
chmod 600 test/blackbox/mail_2_rmq/config/rabbitmq_2.py
vim test/blackbox/mail_2_rmq/config/rabbitmq_2.py
```

Add two email aliases to allow functional testing.
  * Add the following lines to the aliases file:
    - `mailrabbit: "|{DIR_PATH}/mail-rabbitmq/mail_2_rmq.py -c rabbitmq -d {DIR_PATH}/mail-rabbitmq/test/blackbox/mail_2_rmq/config -M"`
    - `mailrabbit_2:   "|{DIR_PATH}/mail-rabbitmq/mail_2_rmq.py -c rabbitmq_2 -d {DIR_PATH}/mail-rabbitmq/test/blackbox/mail_2_rmq/config -M"`

```
sudo vim /etc/aliases
sudo newaliases
```

Add links to the program in the /etc/smrsh directory.

```
cd /etc/smrsh
sudo ln -s {DIR_PATH}/mail-rabbitmq/mail_2_rmq.py mail_2_rmq.py
```

### Testing:

```
mail-rabbitmq/test/blackbox/mail_2_rmq/mail_2_rmq_functional_test.sh
```

### Post-Testing Cleanup:

```
test/blackbox/mail_2_rmq/mail_2_rmq_cleanup.py
```

