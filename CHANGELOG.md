# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


## [0.3.3] - 2019-02-12
### Changed
- main:  Refactored code.
- check_nonprocess:  Changed "LOG" to "log".
- process_message:  Changed "LOG" to "log".
- connect_process:  Changed "LOG" to "log" and "RQ" to "rq".
- archive_email:  Changed "LOG" to "log" and "RQ" to "rq".


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
- run_program:  Changed Single_Instance_Exception to SingleInstanceException.
- run_program:  Changed Program_Lock to ProgramLock.
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
- Parse_Email:  Added function.
- Check_Nonprocess:  Added function stub holder.
- Archive_Email:  Added function stub holder.

### Changed
- main:  Allow the processing of different options from the command line.
- Run_Program:  Call different functions based on options selected.
- Process_Message:  Checks on RabbitMQ connection status.


## [0.0.2] - 2017-11-13
### Added
- Process_Message:  Added function.


## [0.0.1] - 2017-11-10
### Added
- mail:  Added function.
- Run_Program:  Added function.
- Help_Message:  Added function.
