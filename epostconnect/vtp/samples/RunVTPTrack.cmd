@echo off

REM  ***************************************************************************************************************************************
REM  *
REM  *  This file issues a VTP tracking request for the specified account.  It will return all tracked messages on record for the account
REM  *  via a tracking response log located in the "%VTP_HOME/logs" directory.
REM  *
REM  *  Message structure:
REM  *  ------------------
REM  *
REM  *  call %VTP_HOME%/bin/VtpTrack -a <sender account token>
REM  *
REM  *  Parameters:
REM  *  -----------
REM  *   %VTP_HOME% 	- The location of the VTP package; as configured in the "setenv_new.bat" file
REM  *   sender account token - The sending account for which the messages are being tracked
REM  *
REM  *  How to use:
REM  *  -----------
REM  *
REM  *  Modify the following in the command line structure below:
REM  *
REM  *  <server account token> -> replace with your epost connect account provided to you for use with VTP
REM  *  example:  %VTP_HOME%/bin/VtpTrack -a mytokenname
REM  * 
REM  *  Launch the DOS command line by:
REM  *  'double-clicking' on this file from the file browser view
REM  *  
REM  *  Output:
REM  *  -------
REM  *   The "%VTP_HOME/logs" directory will contain two logs after execution: 'tracking-<date-time>.log' and 'exception-<date-time>
REM  *   The tracking log will contain the messages sent by the account and their relative status'; if there were no messages sent successfully
REM  *  the file will be blank.  If there is an error in execution, the exception log will indicate the reason for failure; otherwise, the
REM  *  exception file will be blank,indicating successful execution.
REM  * 
REM  ***************************************************************************************************************************************

call setenv_new
@echo on

%VTP_HOME%/bin/VtpTrack -a <sender account token>

pause 