#!/bin/bash
# Unit test code coverage for SonarQube to cover all modules.
# This will run the Python code coverage module against all unit test modules.
# This will show the amount of code that was tested and which lines of code
#	that was skipped during the test.

coverage erase

echo ""
echo "Running unit test modules in conjunction with coverage"
coverage run -a --source=mail_2_rmq test/unit/mail_2_rmq/help_message.py
coverage run -a --source=mail_2_rmq test/unit/mail_2_rmq/load_cfg.py
coverage run -a --source=mail_2_rmq test/unit/mail_2_rmq/parse_email.py
coverage run -a --source=mail_2_rmq test/unit/mail_2_rmq/archive_email.py
coverage run -a --source=mail_2_rmq test/unit/mail_2_rmq/connect_process.py
coverage run -a --source=mail_2_rmq test/unit/mail_2_rmq/process_message.py
coverage run -a --source=mail_2_rmq test/unit/mail_2_rmq/check_nonprocess.py
#coverage run -a --source=mail_2_rmq test/unit/mail_2_rmq/run_program.py
#coverage run -a --source=mail_2_rmq test/unit/mail_2_rmq/main.py

echo ""
echo "Producing code coverage report"
coverage combine
coverage report -m
coverage xml -i

