@echo off

REM  ***************************************************************************************************************************************
REM  *
REM  *  This file illustrates the creation of a single message with a message and '-i' key specified which embeds the message (up to a MAX
REM  *  of 500 characters) to the content of the notification email.
REM  * 
REM  *
REM  *  Message structure:
REM  *  ------------------
REM  *
REM  *  %VTP_HOME%/bin/VtpSend -s <Subject String> -a <sender account token> -to <email Address> -m <file containing message text> -i
REM  * 
REM  *
REM  *  Parameters:
REM  *  -----------
REM  *   Subject String - The subject string for the message/conversation
REM  *   sender account token - The sending account token for the server
REM  *	 email Address	- The receiver's email address
REM  *   file containing message text - The location of a .txt file containing the message text
REM  *
REM  *
REM  *  How to use:
REM  *  -----------
REM  *
REM  *  Modify the following in the command line structure below:
REM  *
REM  *  <server account token> -> replace with your epost connect account provided to you for use with VTP
REM  *  example:  -a mytokenname
REM  *
REM  *  <email Address> -> replace with intended recipient's email address
REM  *  example:  -to mytest@yahoo.com
REM  * 
REM  *  Launch the DOS command line by:
REM  *  'double-clicking' on this file from the file browser view
REM  *  
REM  *  Output:
REM  *  -------
REM  *   The "%VTP_HOME/logs" directory will contain two logs after execution: 'output-<date-time>.log' and 'exception-<date-time>'
REM  *   The output log will contain details on the message that was sent and whether it was successful.  
REM  *  If there is an error in execution, the exception log will indicate the reason for failure; otherwise, the exception file will 
REM  *  be blank,indicating successful execution.
REM  *
REM  *  The notification message received from the email address specified will contain a message box with text inside
REM  * 
REM  ***************************************************************************************************************************************

call setenv_new

@echo on

call %VTP_HOME%/bin/VtpSend -s "Message in notification email test" -a <sender account token> -to <email Address> -m Files/message2.txt -i

pause