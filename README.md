# Encrypted-Communication-Channel
Encrypt Communication over UDP using securely generated keys for AES
1. Client and Server files for alice and bob
2. A function for generating public numbers of both client and server
3. A timer for computing cipher execution duration
4. Excel Sheet showing the execution time comparision.
5. UDP socket with a dynamic port number
6. A buffer size of 1024 bytes

Execution:

1. Run the Server program first.
2. Run the client program.
3. Time execution will be calculated and printed on screen.
4. Message exchange between alice and Bob (both encrypted and plain text will be printed on screen)

IMPORTANT:

UDP Port number can be different on different computers. If you face difficulty executing the program with provided port numbers,
Please use an open port of your computer system.

Command to find Port number: 
Windows:  netstat -an | findstr ":port number"
Linux:	  netstat -plnt | grep ':port number'
