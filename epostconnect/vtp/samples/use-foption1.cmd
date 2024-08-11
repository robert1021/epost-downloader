@echo off

REM  ***************************************************************************************************************************************
REM  *
REM  *  This file illustrates the use of the '-f' option of the VTP send application.  The '-f' option allows the creation of seperate
REM  *  messages with different subject lines/conversations, message text and attachments to be sent to different recipients.  In this 
REM  *  example, the file containing the different messages is located in the local directory and is named "inputFile.txt".  See contents
REM  *  of "inputFile.txt" to determine the structure required of this file (namely one message description complete with parameters per line)
REM  *   
REM  *  In addition to the use of the '-f'key, this file also illustrates the creation of user defined names/locations for the log and 
REM  *  exception files.
REM  *
REM  *  Message structure:
REM  *  ------------------
REM  *
REM  *  %VTP_HOME%/bin/VtpSend -f <input file> -a <sender account token>
REM  *
REM  *  Parameters:
REM  *  -----------
REM  *   input file	- Name of the file containing the separate message command lines
REM  *   sender account token - The sending account token for the server
REM  *
REM  *  How to use:
REM  *  -----------
REM  *
REM  *  Modify the following in the command line structure below:
REM  *
REM  *  <server account token> -> replace with your epost connect account provided to you for use with VTP
REM  *  example:  -a mytokenname
REM  *
REM  *
REM  *  Modify the following in input file ($VTP_HOME/samples/Files/inputFile.txt):
REM  *  
REM  *  <email_address1> -> Change to a valid email address 
REM  *  <email_address2> -> Change to a valid email address
REM  *  example: -to myemail@yahoo.com
REM  *
REM  *  Launch the DOS command line by:
REM  *  'double-clicking' on this file from the file browser view
REM  *  
REM  *  Output:
REM  *  -------
REM  *   The "%VTP_HOME/logs" directory will contain two logs after execution: 'output-<date-time>.log' and 'exception-<date-time>
REM  *   The output log will contain details on both messages that were sent and whether each was successful.  
REM  *  If there is an error in execution, the exception log will indicate the reason for failure; otherwise, the exception file will 
REM  *  be blank,indicating successful execution.
REM  *
REM  *  Note that while using the '-f' key it is possible to have some messages fail and others pass (i.e. each message is treated independently)
REM  *
REM  ***************************************************************************************************************************************

call setenv_new

@echo on

call %VTP_HOME%/bin/VtpSend -f Files/inputFile.txt -a <server account token> 

pause