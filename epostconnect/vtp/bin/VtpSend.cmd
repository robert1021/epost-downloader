@echo off
setlocal
if "%VTP_HOME%" == "" set VTP_HOME=..

set VTP_HOME=C:/Users/MTEKIEH/Documents/GitHub/parser-extension/Modules/ePost/epostconnect/vtp

%VTP_HOME%\jvm\jre1.8.0_101\bin\java -Djdk.tls.client.protocols="TLSv1.2" -classpath "%VTP_HOME%/lib/*" -DVTP_HOME=%VTP_HOME% epost.connect.vtp.VtpSend %*
endlocal
