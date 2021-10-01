# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


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
- process_message:  Refactored function and added ability to process emails based on the email's From address.
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
