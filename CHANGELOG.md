# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


## [2.2.2] - 2025-09-16

### Fixed
- process_from_debug: Fixed the arguments being passed to the connect_rmq_debug.

### Added
- pub_to_rmq_debug: Consolidate arguments for the call to RMQ and clean up file.


## [2.2.1] - 2025-09-12

### Added
- convert_bytes_debug: Converts a string to bytes.

### Fixed
- convert_bytes: Only convert if a string.
- process_attach, process_attach_debug: Added check to see if the message body was converted to bytes before proceeding.
- process_from_debug: Passed the debug arguments to the connect_rmq_debug call.
- Fixed a number of duplicate debug statements.

### Changed
- Documentation changes.


## [2.2.0] - 2025-09-05
- Added debugging capability using the from address option.
- Updated python-lib to v4.0.3
- Updated rabbitmq-lib v2.4.1

### Added
- process_debug: Process for debugging, used to determine whether to process on subject, from address or attachment.
- archive_email_debug: Save an email to file in an archive directory.
- connect_process_debug: Publish email message to RabbitMQ.
- connect_rmq_debug: Set up and connect to RabbitMQ, check for connection problems.
- get_text_debug: Walks the tree of a email and returns the text of the email.
- process_attach_debug: Locate, extract, and process attachment from email based on specified attachment types.
- process_file_debug: Process email with a file attachment or process as an invalid message.
- process_from_debug: Process email using its From line.
- process_subj_debug: Process email using its subject line and open connection and validate connection to RabbitMQ.

### Changes
- process_message: Added check to see if the mail from address is the debugging email address.
- config/rabbitmq.py.TEMPLATE: Added debugging entries.
- process_attach: Removed the check on if the attachment is a text file to not decode the payload.
- Documnetation changes.

### Deprecated
- Support for RabbitMQ v3.6


## [2.1.0] - 2025-06-24
- Added additional checks when the attachment is a text file.
- Added process ID to all log entries to be able to track each run of the program.
- Updated python-lib to v4.0.2

### Changes
- Added os.getpid to the log class entries.
- archive_email: Minor refactor of function.
- process_attach: Added check ensure attachment has a filename associated and if the attachment is a text file to not decode the payload.
- get_text: Added check to see if content_type is text, otherwise ignore.
- run_program: Minor refactor of function.
- Documentation changes.

### Fixed
- connect_rmq: Only close a RabbitMQ connection if is active.
- filter_subject: Removed loop as it overwriting the previous subject.
- config/rabbitmq.py.TEMPLATE: subj_filter - Changed list to a string.

### Removed
- get_email_addr function.


## [2.0.1] - 2025-06-10
- Updated python-lib to v4.0.1
- Updated rabbitmq-lib v2.4.0

### Fixed
- process_attach: Fixed having problem removing a file during the gen_libs.rm_file call.
- run_program: Removed gen_class.ProgramLock due to the program possibly skipping emails when a lock is in place.

### Changed
- Documentation changes.


## [2.0.0] - 2025-01-24
Breaking Changes

- Removed support for Python 2.7.
- Updated urllib3==1.26.20
- Added certifi==2024.12.14
- Updated python-lib v4.0.0
- Updated rabbitmq-lib v2.3.0

### Fixed
- get_text: Converted byte string to character string if detected.

### Changes
- process_attach: Refactored io.open call.
- connect_rmq: Replaced dict() with {}.
- process_attach: Replaced list() with [].
- Converted strings to f-strings.
- convert_bytes, parse_email: Removed Python 2.7 code.
- Documentation changes.


## [1.5.6] - 2024-11-19
- Updated python-lib to v3.0.8
- Updated rabbitmq-lib to v2.2.8

### Fixed
- Set chardet==3.0.4 for Python 3.


## [1.5.5] - 2024-11-12
- Updated chardet==4.0.0 for Python 3.
- Updated distro==1.9.0 for Python 3.
- Added idna==2.10 for Python 3.
- Updated pika==1.3.1 for Python 3.
- Updated psutil==5.9.4 for Python 3.
- Updated requests==2.25.0 for Python 3.
- Updated urllib3==1.26.19 for Python 3.
- Updated six==1.16.0 for Python 3.
- Updated python-lib to v3.0.7
- Updated rabbitmq-lib to v2.2.7

### Deprecated
- Support for Python 2.7


## [1.5.4] - 2024-09-27
- Updated simplejson==3.13.2 for Python 3
- Updated python-lib to v3.0.5
- Updated rabbitmq-lib to v2.2.6


## [1.5.3] - 2024-08-15

### Fixed
- process_file: Added connect_rmq call if subject is in the file_queues list.


## [1.5.2] - 2024-08-07
- Updated simplejson==3.13.2
- Updated requests==2.25.0
- Added certifi==2019.11.28
- Added idna==2.10
- Removed email==4.0.3
- Updated rabbitmq-lib to v2.2.5

### Changed
- Updates to requirements.txt.


## [1.5.1] - 2024-07-30
- Set urllib3 to 1.26.19 for Python 2 for security reasons.
- Updated rabbitmq-lib to v2.2.4


## [1.5.0] - 2024-06-17
- Pass filename along with attachment to RabbitMQ.
- Cleaned up the connection and publishing process.

### Added
- connect_rmq: Set up and connect to RabbitMQ, check for connection problems.

### Changed
- main: Removed parsing from gen_class.ArgParser call and called arg_parse2 as part of "if" statement.
- process_file, process_subj, process_from: Removed code to replace with call to connect_rmq function.
- connect_process: Inserted a file into a dictionary along with its filename.
- connect_process: Removed the connection call, this moved to the calling functions - see below.
- process_subj, process_from, process_file:  Added connection call and check to function.


## [1.4.2] - 2024-24-24
### Fixed
- process_attach: Added log entry to display attachment type if attachment is detected as invalid.

### Changed
- config/rabbitmq.py.TEMPLATE: Added "text/csv" to allowable attachments in attach_types.


## [1.4.1] - 2024-03-06
- Updated to work in Red Hat 8
- Updated rabbitmq-lib to v2.2.3
- Updated python-lib to v3.0.3

### Changed
- run_program:  Removing some of the lines from the log preamble.
- config/rabbitmq.py.TEMPLATE:  Added application/octet-stream to attach_types.
- process_attach: Printing to log the content_type of the attachment.
- Set simplejson to 3.12.0 for Python 3.
- Set chardet to 3.0.4 for Python 2.
- Documentation updates.


## [1.4.0] - 2023-10-10
- Replaced the arg_parser code with gen_class.ArgParser code.

### Changed
- Multiple functions: Replaced the arg_parser code with gen_class.ArgParser code.
- main, run_program, parse_email: Removed gen_libs.get_inst call.
- Documentation updates.


## [1.3.2] - 2022-12-09
- Updated to work in Python 3 too
- Upgraded python-lib to v2.9.4
- Upgraded rabbitmq-lib to v2.2.1

### Changed
- Converted imports to use Python 2.7 or Python 3.
- process_message: Changed output of dictionary keys call to a list.
- process_attach: Replaced open() call with io.open() call and called convert_bytes to convert data to bytes if in Python 3.
- parse_email: Using different email parsers depending on Python version.

### Added
- convert_bytes: Converts a string to bytes if in a Python 3 environment.


## [1.3.1] - 2021-11-19
- Upgrade python-lib to v2.9.2
- Upgrade rabbitmq-lib to v2.2.0

### Fixed
- run_program: Appended the date to the end of the log files for daily log rotation.
- connect_process: Email body returns text or an empty string.

### Changed
- process_message: Replaced camelize with gen_libs.pascalize call and replaced get_email_addr with gen_libs.find_email_addr call.
- Documentation update.

### Removed
- get_email_addr:  Replaced with gen_libs.find_email_addr call.
- camelize:  Replaced with gen_libs.pascalize call.


## [1.3.0] - 2021-09-28
- Update to work with Pika 1.2.0
- Update to work with RabbitMQ 3.8.2
- Added ability to handle connecting to multiple node cluster

### Added
- process_file:  Process email with a file attachment or process as an invalid message.
- process_from:  Process email using its From line.
- process_subj:  Process email using its subject line.
- get_email_addr:  Finds all email addresses in the data string.

### Changed
- process_attach:  Add ability to capture multiple attachments in an email.
- process_message:  Refactored function and added ability to process emails based on the emails From address.
- config/rabbitmq.py.TEMPLATE:  Added heartbeat, host_list, err_addr_queue and queue_dict entries.
- Documentation updates.

### Removed
- create_rq function


## [1.2.0] - 2021-07-12
### Changed
- process_message:  Added check to process and send file attachments to specify queues.
- config/rabbitmq.py.TEMPLATE:  Added file_queues and err_file_queue, and removed file_queue.
- run_program:  Added information about file queues to the log information.
- Removed unnecessary \*\*kwargs in function argument list.
- Documentation updates.


## [1.1.0] - 2020-09-16
### Added
- Added -y option to create unique program lock flavor id.
- process_attach:  Locate, extract, and process attachment from email based on specified attachment types.
- config/rabbitmq.py.TEMPLATE:  Added file_queue, tmp_dir, and attach_types entries.

### Changed
- run_program:  Captured error messages from load_cfg and processed them.
- load_cfg:  Returned err_msg from gen_libs.chk_crt_dir to calling function.
- load_cfg:  Added configuration setting tmp_dir to directory check.
- run_program:  Setup flavor_id to use -y option value or exchange_name as a default.
- main:  Added -y option to the setup.
- run_program:  Refactored status_flag check.
- create_rq:  Changed configuration settings to reflect changes in config file.
- process_message:  Added call to process_attach and process any attachment found.
- connect_process:  Added ability to process file attachment in an email.
- config/rabbitmq.py.TEMPLATE:  Changed entry in configuration file.
- Documentation updates.


## [1.0.0] - 2020-07-08
- General Production Release

### Fixed
- parse_email, run_program, main:  Fixed handling command line arguments.

### Changed
- create_rq:  Changed positional args for rabbitmq_class.RabbitMQPub to kwargs.
- process_message, connect_process, archive_email, parse_email:  Changed variable names to standard naming convention.
- config/rabbitmq.py.TEMPLATE:  Changed format.
- Documentation updates.


## [0.3.6] - 2019-05-08
### Fixed
- run_program:  Fixed problem with mutable default arguments issue.

### Added
- camelize:  PascalCase a string.
- create_rq:  Function to create and return a RabbitMQ instance.

### Changed
- process_message:  Refactored, added camelize call on subject, and replaced create instance with create_rq call.


## [0.3.5] - 2019-03-01
### Added
- filter_subject:  Filters strings out of the message subject line.

### Changed
- archive_email:  Replaced "open()" with call to "gen_libs.write_file".
- run_program, process_message:  Changed variable names to standard naming convention.
- run_program:  Moved program lock from inside for loop to outside of for loop.
- process_message:  Added function call to filter_subject, replaced msg['subject'] with subj.


## [0.3.4] - 2019-02-19
### Added:
- get_text:  Walks the tree of an email to return text from a multi-part email.

### Changed
- connect_process:  Replaced "msg.get_payload" with call to get_text function.
- parse_email:  Replaced "email" class with "email.Parser" class.


## [0.3.3] - 2019-02-12
### Changed
- main:  Refactored code.
- check_nonprocess, process_message, connect_process, archive_email:  Changed variable names to standard naming convention.


## [0.3.2] - 2018-11-19
### Changed
- Documentation updates.


## [0.3.1] - 2018-05-14
### Changed
- load_cfg:  Refactored code to use gen_libs.chk_crt_dir function.
- Changed "gen_libs" calls to new naming schema.
- Changed "arg_parser" calls to new naming schema.
- Changed lclass to rabbit_lib for standardization.


## [0.3.0] - 2018-05-04
- Field release.


## [0.2.1] - 2018-02-27
### Added
- Add single source version control to program.

### Changed
- run_program:  Changed Single_Instance_Exception to SingleInstanceException and changed Program_Lock to ProgramLock.
- archive_email:  Added ".email.txt" to archive email file name.


## [0.2.0] - 2017-12-07
- Beta release

### Changed
- Documentation updates.


## [0.1.4] - 2017-12-06
### Changed
- Documentation updates.


## [0.1.3] - 2017-11-24
### Changed
- Help_Message:  Updated documentation in help.


## [0.1.2] - 2017-11-23
### Fixed
- Connect_Process: Publish entire email if going to error queue, otherwise just email body.
- Process_Message: Pass email instance to Connect_Process instead of email body.


## [0.1.1] - 2017-11-20
### Fixed
- Process_Message:  Passing string to Connection_Process call instead of mail instance.


## [0.1.0] - 2017-11-17
- Alpha release

### Fixed
- Archive_Email:  Changed exchange_name to exchange.


## [0.0.5] - 2017-11-16
### Changed
- Archive_Email:  Write email out to file.
- Run_Program:   Add additional Logging information entry.
- Archive_Email:   Add logging statements.

### Fixed
- Connect_Process:  Correct syntax errors.
- Load_Cfg:  Removed check on path_dir.


## [0.0.4] - 2017-11-15
### Changed
- main:  Setup checks for -M and -C options as XOR.
- Run_Program:  Moved program lock to within function loop.
- Run_Program:  Add logger class instance.
- Process_Message:  Check email subject for valid queue.
- Process_Message:  Add logger entries.
- Archive_Email:  Change interface arguments.

### Added
- Load_Cfg:  Added function to check configuration file.
- Connect_Process:  Added function to connect to RabbitMQ node.


## [0.0.3] - 2017-11-14
### Added
- Parse_Email
- Check_Nonprocess
- Archive_Email

### Changed
- main:  Allow the processing of different options from the command line.
- Run_Program:  Call different functions based on options selected.
- Process_Message:  Checks on RabbitMQ connection status.


## [0.0.2] - 2017-11-13
### Added
- Process_Message


## [0.0.1] - 2017-11-10
### Added
- mail
- Run_Program
- Help_Message
