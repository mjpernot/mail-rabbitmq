# RabbitMQ Configuration file
# Classification (U)
# Unclassified until filled.
user = "<USER>"
passwd = "<PASSWORD>"
host = "<HOSTNAME>"
# RabbitMQ Exchange name for each instance run.
exchange_name = "isse-guard-test"
# List of valid queues in RabbitMQ.
valid_queues = [ "SIPR-test", "SG-test" ]
# Name of error queue to handle incorrectly routed emails.
err_queue = "isse_error_test"
# Archive directory path for non-processed email files.
email_dir = "./test/unit/mail_2_rmq/email_dir"
# Directory path and file name to the program log.
log_file = "./test/unit/mail_2_rmq/logs/mail_2_rmq.log"
# RabbitMQ listening port, default is 5672.
port = 5672
# Type of exchange:  direct, topic, fanout, headers
exchange_type = "direct"
# Is exchange durable: True|False
x_durable = True
# Are queues durable: True|False
q_durable = True
# Do queues automatically delete once message is processed:  True|False
auto_delete = False

