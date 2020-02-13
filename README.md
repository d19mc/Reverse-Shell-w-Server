# Reverse-Shell-w-Server
This is a RAT that also includes a Phishing attack with a fake Blue Screen of Death screen using the module Tkinter. An admin_client.py was made which was abset in the original Reverse-Shell and now takes the place of the server in the original Reverse-Shell. Essentially sending commands to the real victim of the attack. The server in this repo is what is implies. Just a server that transfers bytes between the 2 clients {admin + selected client}. The server also logs out what is happening on the server. 

Future Plans:
- Add Phishing Outlook Sign-in to the RAT
- Gain access to contacts through above Phishing attack and spread malware to selected people

This could cause a lot of damage on systems. A bit of social engineering required to place file on victims computer but due to the server capabilites of accessing any device from anywhere, you can transfer a file from your device (payload) onto the victims device on any folder with user access (like User startup) to confirm eternal control of targetted PC.

This is mainly targetted towards windows PCs. It is functional on Macbooks but there is no way to start this up on startup.

