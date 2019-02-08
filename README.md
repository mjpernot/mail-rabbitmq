# Python project for the processing of emails to be injested into RabbitMQ.
# Classification (U)

# Description:
  This project is used to process and parse emails that are injested into a queue in RabbitMQ.


###  This README file is broken down into the following sections:
  * Features
  * Prerequisites
  * Installation
  * Configuration
  * Mail Alias Setup
  * Program Description
  * Program Help Function
  * Help Message
  * Testing
    - Unit
    - Blackbox

# Features:
  * Process and parse emails via mailing pipe.
  * Insert email into correct RabbitMQ queue based on email subject line.

# Prerequisites:

  * List of Linux packages that need to be installed on the server.
    - python-libs
    - python-devel
    - git
    - python-pip

  * Local dependencies within the program structure.
    - lib/gen_class
    - lib/arg_parser
    - lib/gen_libs
    - rabbit_lib/rabbitmq_class

  * Setup a local account and group: rabbitmq:rabbitmq


# Installation:

Install the program using git 
  * Replace **{Python_Project}** with the baseline path of the python program.
```
umask 022
cd {Python_Project}
git clone git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/mail-rabbitmq.git
```

Install/upgrade system modules.
```
cd mail-rabbitmq
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.
```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-rabbitmq-lib.txt --target rabbit_lib --trusted-host pypi.appdev.proj.coe.ic.gov
```


# Configuration:

Setup configuration file.

```
chmod 777 email_dir logs
cd config
cp rabbitmq.py.TEMPLATE rabbitmq.py
```

Make the appropriate changes to the RabbitMQ environment in the rabbitmq.py file.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * "user", "passwd", and "host" is connection information to a RabbitMQ node.
  * "exchange_name" is name of the exchange in the RabbitMQ node.
  * "valid_queues" is a list of queue names in the RabbitMQ node, the queue names are direct correlation to the subject names in the emails.
  * "err_queue" is the name of RabbitMQ queue that will contain any messages that do not fit in the other queues (i.e. invalid subject lines).
  * "email_dir" is the location where non-processed emails will be saved to (e.g. when RabbitMQ is down).
  * "log_file" is the location of the mail_2_rmq.py log file.
    - user = "USER"
    - passwd = "PASSWORD"
    - host = "HOSTNAME"
    - exchange_name = "EXCHANGE_NAME"
    - valid_queues = ["QUEUE_NAME1", "QUEUE_NAME2"]
    - err_queue = "ERROR_QUEUE_NAME"
    - email_dir = "{Python_Project}/mail_rabbitmq/email_dir"
    - log_file = "{Python_Project}/mail_rabbitmq/logs/mail_2_rmq.log"

```
vim rabbitmq.py
chmod 600 rabbitmq.py
```


# Mail Alias Setup
  * If installing on a postfix system, use the **"Postfix system"** option.  Otherwise use the **"Alias system"** option for all other systems.

### Postfix system

Setup local aliases for rabbitmq account:
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Add to the file:
    -  rabbitmq: "|{Python_Project}/mail-rabbitmq/mail_2_rmq.py -c rabbitmq -d {Python_Project}/mail-rabbitmq/config -M"
```
vim /home/rabbitmq/.aliases
```

Change ownership of configuration file.
```
sudo chown rabbitmq:rabbitmq {Python_Project}/mail-rabbitmq/config/rabbitmq.py
```

In a second term window:
  * Monitor the system messages file for an SELinux policy exceptions.
```
sudo tail -f /var/log/messages
```

Create aliases database in first term window (run as rabbitmq).
```
postalias .aliases
```

Monitor the messages file for SELinux exceptions, look for "run sealert".  NOTE:  Most audit logs rotate every 10 minutes, so if the sealert command fails, re-run the email message in again.
  * HexiDecimal_Key will be displayed in the tail command in the second term window.
```
sudo sealert -l {HexiDecimal_Key}
```

Run the grep and sedmodule commands from sealert command.  Example below.
```
sudo bash
cd /root
grep mail_2_rmq.py /var/log/audit/audit.log | audit2allow -M mypol
semodule -i mypol.pp
exit
```

Re-create the aliases database, if SELinux policy exception was detected and removed (run as rabbitmq).
```
postalias .aliases
```

Setup aliases in main.cf file.
  * Replace **{HOME}** with the baseline path to the rabbitmq's home directory.
  * Add the following lines to the file:
    -  `alias_maps = hash:/{HOME}/rabbitmq/.aliases`
    -  `alias_database = hash:/{HOME}/rabbitmq/.aliases`
```
sudo vim /etc/postfix/main.cf
```

Reload postfix.
```
sudo service postfix restart
```

Allow the access to .aliases and .aliases.db files.
  * Replace **{HOME}** with the baseline path to the rabbitmq's home directory.
```
sudo bash
semanage fcontext -a -t etc_aliases_t "/{HOME}/rabbitmq/\.aliases"
restorecon -R /{HOME}/rabbitmq/.aliases
semanage fcontext -a -t etc_aliases_t "/{HOME}/rabbitmq/\.aliases.db"
restorecon -R /{HOME}/rabbitmq/.aliases.db
exit
```

In second term window:
  * Continue monitoring the system messages file for an SELinux policy exceptions.
```
sudo tail -f /var/log/messages
```

Send test email to rabbitmq.
```
echo "sipr-isse" | mailx -s sipr-isse rabbitmq@mail.eu.dodiis.ic.gov
```

Monitor the messages file for SELinux exceptions, look for "run sealert".
  * NOTE:  Most audit logs rotate every 10 minutes, so if the sealert command fails, re-run the email message in again.
  * HexiDecimal_Key will be displayed in the tail command in the second term window.
```
sudo sealert -l {HexiDecimal_Key}
```

Run the grep and sedmodule commands from sealert command.  Example below.
```
sudo bash
cd /root
grep mail_2_rmq.py /var/log/audit/audit.log | audit2allow -M mypol
semodule -i mypol.pp
exit
```

Repeat the previous three steps (from "Send test email to rabbitmq" onward) until all exceptions have been found and excluded in the policy.


### Alias system
  * This will only work on non-postfix systems.

Add an email alias to allow mail piping.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Add the following entry:
    - `mailrabbit: "|{Python_Project}/mail_rabbitmq/mail_2_rmq.py -c rabbitmq -d {Python_Project}/mail_rabbitmq/config -M"`
```
sudo vim /etc/aliases
sudo newaliases
```

Add links to the program in the /etc/smrsh directory.
```
cd /etc/smrsh
sudo ln -s {Python_Project}/mail_rabbitmq/mail_2_rmq.py mail_2_rmq.py
```

Change ownership of configuration file.
```
sudo chown mail:mail {Python_Project}/mail_rabbitmq/config/rabbitmq.py
```


# Program Description:
### Program:  mail_2_rmq.py
##### Description:  Process an email message and send it to the proper RabbitMQ queue.


# Program Help Function:

  The program has a -h (Help option) that will show display an usage message.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:
  * Replace **{Python_Project}** with the baseline path of the python program.
```
{Python_Project}/mail-rabbitmq/mail_2_rmq.py -h
```


# Help Message:
  Below is the help message for the program.  Recommend running the -h option on the command line to see the latest help message.

    Program:  mail_2_rmq.py

    Description:  Process an email message and send it to the proper
        RabbitMQ queue.

    Usage:
        -M option
        email_alias: "| /{directory_path}/mail_2_rmq.py -M -c file -d path"

        All other options.
        mail_2_rmq.py [-C] [-c file -d path] [-v | -h]

    Arguments:
        -M => Receive email messages from email pipe and process.
        -C => Check for non-processed messages in email archive directory.
        -c file => ISSE Guard configuration file.  Required argument.
        -d dir path => Directory path for option '-c'.  Required argument.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1:  -v or -h overrides all other options.
        NOTE 2:  -M and -C are XOR options.

    Notes:
        The configuration file below is required to run this program.  Create
        them and replace those variables (i.e. <VARIABLE>) with a value.

        Configuration file format (rabbitmq.py).  The configuration file format
        is for the initial environment setup for the program.
            # RabbitMQ Configuration file
            # Classification (U)
            # Unclassified until filled.
            user = "<USER>"
            passwd = "<PASSWORD>"
            host = "<HOSTNAME>"
            # RabbitMQ listening port, default is 5672.
            port = 5672
            # RabbitMQ Exchange name for each instance run.
            exchange_name = "<EXCHANGE_NAME>"
            # Type of exchange:  direct, topic, fanout, headers
            exchange_type = "direct"
            # Is exchange durable: True|False
            x_durable = True
            # Are queues durable: True|False
            q_durable = True
            # Do queues delete once message is processed:  True|False
            auto_delete = False
            # List of valid queues in RabbitMQ.
            valid_queues = [ "QUEUE_NAME1", "QUEUE_NAME2", ... ]
            # Name of error queue to handle incorrect email subjects.
            err_queue = "<ERROR_QUEUE_NAME>"
            # Archive directory path for non-processed email files.
            email_dir = "/<DIRECTORY_PATH>/email_dir"
            # Directory path and file name to the program log.
            log_file = "/<DIRECTORY_PATH>/logs/mail_2_rmq.log"

    Example:
        /opt/local/mail_2_rmq.py -C -c rabbitmq -d /opt/local/config"

        email_alias: "| /opt/local/mail_2_rmq.py -M -c rabbitmq -d /opt/local/config"


# Testing:

# Unit Testing:

### Description: Testing consists of unit testing for the functions in the mail_2_rmq.py program.

### Installation:

Install the program using git 
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.
```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/mail-rabbitmq.git
```

Install/upgrade system modules.
```
cd mail-rabbitmq
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.
```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-rabbitmq-lib.txt --target rabbit_lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

# Unit test runs for mail_2_rmq.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

### Individual Unit Tests:
```
cd {Python_Project}/mail-rabbitmq
test/unit/mail_2_rmq/load_cfg.py
test/unit/mail_2_rmq/parse_email.py
test/unit/mail_2_rmq/archive_email.py
test/unit/mail_2_rmq/connect_process.py
test/unit/mail_2_rmq/process_message.py
test/unit/mail_2_rmq/check_nonprocess.py
test/unit/mail_2_rmq/help_message.py
test/unit/mail_2_rmq/run_program.py
```

### All unit tests:
```
test/unit/mail_2_rmq/unit_test_run.sh
```


# Blackbox Testing:

### Description: Testing consists of blackbox testing of the mail_2_rmq.py program.

### Installation:

Install the program using git 
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.
```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/mail-rabbitmq.git
```

Install/upgrade system modules.
```
cd mail-rabbitmq
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.
```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-rabbitmq-lib.txt --target rabbit_lib --trusted-host pypi.appdev.proj.coe.ic.gov
```


### Configuration:

Create configuration file for testing.
```
chmod 777 email_dir logs
cd test/blackbox/mail_2_rmq/config
cp ../../../../config/rabbitmq.py.TEMPLATE rabbitmq.py
```

Make the appropriate changes to the RabbitMQ environment in the rabbitmq.py file.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * "user", "passwd", and "host" is connection information to a RabbitMQ node.
  * "exchange_name" is name of the exchange in the RabbitMQ node.
  * "valid_queues" is a list of queue names in the RabbitMQ node, the queue names are direct correlation to the subject names in the emails.
  * "err_queue" is the name of RabbitMQ queue that will contain any messages that do not fit in the other queues (i.e. invalid subject lines).
  * "email_dir" is the location where non-processed emails will be saved to (e.g. when RabbitMQ is down).
  * "log_file" is the location of the mail_2_rmq.py log file.
    - user = "USER"
    - passwd = "PASSWORD"
    - host = "HOSTNAME"
    - exchange_name = "EXCHANGE_NAME"
    - valid_queues = ["QUEUE_NAME1", "QUEUE_NAME2"]
    - err_queue = "ERROR_QUEUE_NAME"
    - email_dir = "{Python_Project}/mail_rabbitmq/email_dir"
    - log_file = "{Python_Project}/mail_rabbitmq/logs/mail_2_rmq.log"
```
vim rabbitmq.py
chmod 644 rabbitmq.py
```

Setup a second configuration file to test non-connection logic paths.
  * Change the same variables as listed except change the passwd variable to an incorrect password.
```
cp rabbitmq.py rabbitmq_2.py
vim rabbitmq_2.py
chmod 644 rabbitmq_2.py
```

Add two email aliases to allow functional testing.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Add the following lines to the aliases file:
    - mailrabbit: "|{Python_Project}/mail-rabbitmq/mail_2_rmq.py -c rabbitmq -d {Python_Project}/mail-rabbitmq/test/blackbox/config -M"
    - mailrabbit_2:   "|{Python_Project}/mail-rabbitmq/mail_2_rmq.py -c rabbitmq_2 -d {Python_Project}/mail-rabbitmq/test/blackbox/config -M"
```
sudo vim /etc/aliases
sudo newaliases
```

Add links to the program in the /etc/smrsh directory.
  * Replace **{Python_Project}** with the baseline path of the python program.
```
cd /etc/smrsh
sudo ln -s {Python_Project}/mail-rabbitmq/mail_2_rmq.py mail_2_rmq.py
```

# Blackbox test run for mail_2_rmq.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

### Blackbox:  mail_2_rmq.py
```
cd {Python_Project}/mail-rabbitmq/test/blackbox
./mail_2_rmq_functional_test.sh
```

#### Post-Testing Cleanup:
```
cd ../..
test/blackbox/mail_2_rmq_cleanup.py
```

