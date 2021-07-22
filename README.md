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

  * List of Linux packages that need to be installed on the server.
    - git
    - python-pip

  * Local dependencies within the program structure.
    - python-lib
    - rabbitmq-lib

  * Setup a local account and group: rabbitmq:rabbitmq


# Installation:

Install the program using git 
  * From here on out, any reference to **{Python_Project}** or **PYTHON_PROJECT** replace with the baseline path of the python program.

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
cd config
cp rabbitmq.py.TEMPLATE rabbitmq.py
vim rabbitmq.py
chmod 600 rabbitmq.py
```


# Mail Alias Setup
  * If installing on a postfix system, use the **"Postfix system"** option.  Otherwise use the **"Alias system"** option for all other systems.
  * Replace **{Python_Project}** with the baseline path of the python program.

### Postfix system

Setup local aliases for rabbitmq account:
  * Add to the file:
    - `rabbitmq: "|{Python_Project}/mail-rabbitmq/mail_2_rmq.py -c rabbitmq -d {Python_Project}/mail-rabbitmq/config -M"`

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
echo "sipr-isse" | mailx -s sipr-isse rabbitmq@mail.domain.name
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


# Program Help Function:

  All of the programs, except the command and class files, will have an -h (Help option) that will show display a help message for that particular program.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
{Python_Project}/rmq-sysmon/mail_2_rmq.py -h
```


# Testing:

# Unit Testing:

### Installation:

Install the project using the procedures in the Installation section.

### Testing:

```
cd {Python_Project}/mail-rabbitmq
test/unit/mail_2_rmq/unit_test_run.sh
```

### Code coverage:

```
cd {Python_Project}/mail-rabbitmq
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
cd test/blackbox/mail_2_rmq/config
cp ../../../../config/rabbitmq.py.TEMPLATE rabbitmq.py
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
  * Add the following lines to the aliases file:
    - `mailrabbit: "|{Python_Project}/mail-rabbitmq/mail_2_rmq.py -c rabbitmq -d {Python_Project}/mail-rabbitmq/test/blackbox/mail_2_rmq/config -M"`
    - `mailrabbit_2:   "|{Python_Project}/mail-rabbitmq/mail_2_rmq.py -c rabbitmq_2 -d {Python_Project}/mail-rabbitmq/test/blackbox/mail_2_rmq/config -M"`

```
sudo vim /etc/aliases
sudo newaliases
```

Add links to the program in the /etc/smrsh directory.

```
cd /etc/smrsh
sudo ln -s {Python_Project}/mail-rabbitmq/mail_2_rmq.py mail_2_rmq.py
```

### Testing:

```
cd {Python_Project}/mail-rabbitmq/test/blackbox/mail_2_rmq
./mail_2_rmq_functional_test.sh
```

### Post-Testing Cleanup:

```
cd {Python_Project}/mail-rabbitmq
test/blackbox/mail_2_rmq/mail_2_rmq_cleanup.py
```

