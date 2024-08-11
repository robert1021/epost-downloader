
@echo off

REM  ***************************************************************************************************************************************
REM  *
REM  *  This CMD file sends a single message to a group of recipients listed in a text file "Files/Customerlist.txt".  The text file contains 
REM  *  a single recipient email address per line.  The CMD file below executes a VTP send command for each email in the file, substituting
REM  *  the value of the variable %email% sequentially as it works its way from top to bottom email in the file.  Note that seperate log and
REM  *  exception files are generated for each of the recipient emails in the file.
REM  *
REM  *  Message structure:
REM  *  ------------------
REM  *
REM  *  %VTP_HOME%/bin/VtpSend -a <sender account token> -s <Subject String> -to %email% -lang <language> -m <file containing message text>
REM  *
REM  *  Parameters:
REM  *  -----------
REM  *   sender account token - The sending account token for the server
REM  *   Subject String - The subject string for the message/conversation
REM  *	 %email%	- The receiver's email address as read in from a text file containing a list
REM  *   language	- The notification email language (en-english or fr-french)
REM  *   file containing message text - The location of a '.txt file' containing the message text
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
REM  *
REM  *  Modify the following in recipient list file ($VTP_HOME/samples/Files/CustomerList.txt):
REM  *  
REM  *  email1@canadapost.ca -> change to valid email address
REM  *  email2@canadapost.ca -> change to valid email address
REM  *  email3@canadapost.ca -> change to valid email address
REM  *  
REM  *  ... Can add other email addresses as required (one per line)
REM  *  ensure that changes to file are saved
REM  *
REM  *  Launch the DOS command line by:
REM  *  'double-clicking' on this file from the file browser view
REM  *  
REM  *  Output:
REM  *  -------
REM  *   The "%VTP_HOME/logs" directory will contain two logs after execution for EACH email address in the 
REM  *   customer List file: 'output-<date-time>.log' and 'exception-<date-time>'.
REM  *  Each output log will contain details on the respective message that was sent and whether it was successful.  
REM  *  If there is an error in execution, the corresponding exception log will indicate the reason for failure; otherwise, the exception file will 
REM  *  be blank,indicating successful execution. 
REM  * 
REM  ***************************************************************************************************************************************

call setenv_new

for /f %%a in (Files/Customerlist.txt) do call :SendPcs %%a
goto END

:SendPcs
set email=%1

@echo on
call %VTP_HOME%/bin/VtpSend  -a <server account token> -s "Email to group" -to %email% -lang en -m Files/message2.txt

:END