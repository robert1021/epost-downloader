RELEASE NOTES

Version: 0.2.0
Release Date: June 12, 2013
User Guide version: 2.6

SYSTEM REQUIREMENTS
-------------------
This installation package is only for Windows platforms. It contains JDK for 
Windows. VTP for UNIX platforms is distributed as separate installation package.

The following is required to install and run the VTP utility:
- Windows XP or higher
- Minimum Memory (RAM): 128 MB
- Minimum Disk Space: 1 GB
- Unzip utility: Windows Winzip, TAR or similar compatible with ZIP compression

A valid epost ConnectTM account and access token is required to run the 
applications. Please contact your Canada Post sales representative to obtain 
this token. The account token is valid for owner's usage only.

RELEASE CONTENTS
----------------
1. Volume Transaction Sending Application (vtpsend) provides the ability to 
create conversations, create and send messages while preserving the core 
functionality of epost ConnectTM.

2. Volume Transaction Tracking Application (vtptrack) provides the ability to 
track data on messages sent by an account.

3. Volume Transaction Receiving Application(vtpreceive) provides the ability to 
download messages in bulk via the epost ConnectTM server.

LIMITATIONS
-----------
1.  The maximum number of recipients per conversation (vtpsend -to) is 3000 
recipients per submission and 5000 recipients per conversation.
2.  The maximum size per attachment file (vtpsend -att) is 2GB.
3.  The maximum size of the personal message (vtpsend -i) is 500 characters.  

KNOWN ISSUES
------------
VTP package for UNIX is not yet available.