@echo off

REM  ***************************************************************************************************************************************
REM  *
REM  *  This file illustrates the creation of a single message with message text and a single '.pdf' file attachment sent to a single recipient
REM  *
REM  *  Message structure:
REM  *  ------------------
REM  *
REM  *  %VTP_HOME%/bin/VtpSend  -a <sender account token> -s <Subject String> -to <email address> -lang <language> -m <file containing message text>
REM  *    -att <attachment file for message>
REM  * 
REM  *
REM  *  Parameters:
REM  *  -----------
REM  *   sender account token - The sending account token for the server
REM  *   Subject String - The subject string for the message/conversation
REM  *	 email Address	- The receiver's email address
REM  *   language	- The notification email language (en-english or fr-french)
REM  *   file containing message text - The location of a .txt file containing the message text
REM  *   attachment file for message  - The location of the file attachment for the message
REM  *
REM  *
REM  *  How to use:
REM  *  -----------
REM  *
REM  *  Modify the following in the command line structure below:
REM  *
REM  *  <sender account token> -> replace with your epost connect account provided to you for use with VTP
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
REM  *   The "%VTP_HOME/logs" directory will contain two logs after execution: 'output-<date-time>.log' and 'exception-<date-time>
REM  *   The output log will contain details on the message that was sent and whether it was successful.  
REM  *  If there is an error in execution, the exception log will indicate the reason for failure; otherwise, the exception file will 
REM  *  be blank,indicating successful execution.
REM  * 
REM  ***************************************************************************************************************************************

call setenv_new

@echo on

call %VTP_HOME%/bin/VtpSend  -a <sender account token> -s "Message with attachment - one recipient" -to <email Address> -lang en -m Files/message.txt -att Files/Zombies.pdf

pause