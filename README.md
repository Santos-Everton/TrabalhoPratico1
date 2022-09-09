![Logo_UFRB](https://www.ufrb.edu.br/ascom/images/marca2017/marca-HORIZONTAL-UFRB-PNG.png)

# GCET-547 Distributed systems - Practical work 1 

#### Professor: Ramon Pereira Lopes
#### Student: Éverton Gomes dos Santos

***

## Client-server TCP multi-thread

***

### Description
The project consists of a TCP client to retrieve files and a TCP server with disk memory and cache memory to provide the files requested by the client.
The client, after establishing a connection with the server, sends the name of the file it requests and if the file is found in any of the locations it is sent through the same connection, caching the contents of the file if it is not cached.
The cache memory contains 64 MB, if the file contains more than 64 MB it is not cached, and if the cache size exceeds 64 MB after placing the file in memory, the cache is cleared to ensure it does not exceed the cache limit. size. 
This server is multi-threaded, that is, several clients can establish connections at the same time and it also has mutual exclusion in case a file is requested by several clients at the same time.

### Architecture and design decisions
The PyCharm IDE (own choice) was used to implement the project with python language as it supports locking and multi-thread naturally with import of some important libraries for applied concepts such as mutual access and multi-clients.
With multi-thread we have to control access to files to avoid corruption. Naturally when a thread is created the primitive state is unlocked, the method `acquire()` changes state to blocked until a call to the method `release()` be done by resetting the status to unlocked.
In addition, cache memory was implemented using the _dictionary_ data structure of the python language, with the file name as a key and the file itself as a value.
Another design decision was made regarding the implementation of a file replacement algorithm in cache memory, since its fixed size is 64 MB. For this, the FIFO logic was used (_first In, first Out_). 
So the first file that was added to the cache will be deleted in case it gives space to other files.
The project directory architecture follows as illustrated below:

| TrabalhoPratico1 |  |  |  |
:---: | :---: | :---: | :---:
| :arrow_right_hook: | __main.pdf__ |  |  |
| :arrow_right_hook: | __venv__ |  |  |
| :arrow_right_hook: | __cliente__ |  |  |
|  | :arrow_right_hook: | __cliente_tcp.py__ |  |
|  | :arrow_right_hook: | __diretorio_cliente__ |  |
| :arrow_right_hook: | __servidor__ |  |  |
|  | :arrow_right_hook: | __servidor_tcp.py__ |  |
|  | :arrow_right_hook: | __diretorio_servidor__ |  |
|  |  | :arrow_right_hook: | __arquivo1.txt__ |
|  |  | :arrow_right_hook: | __arquivo2.txt__ |
|  |  | :arrow_right_hook: | __arquivo3.txt__ |
|  |  | :arrow_right_hook: | __arquivo4.txt__ |
|  |  | :arrow_right_hook: | __arquivo5.txt__ |
|  |  | :arrow_right_hook: | __arquivo6.txt__ |
|  |  | :arrow_right_hook: | __arquivo7.txt__ |
|  |  | :arrow_right_hook: | __pexels-da....jpg__ |
|  |  | :arrow_right_hook: | __Vista_aér....jpeg__ |
|  |  | :arrow_right_hook: | __video.mp4__ |
|  |  | :arrow_right_hook: | __Swimming....mp3__ |
|  |  | :arrow_right_hook: | __Summer_S....mp3__ |

The directory `diretorio_cliente` was created but the user has the possibility to choose the directory to which he wants to save the file by giving the appropriate command. and the directory `venv` is created by the IDE as a virtual environment for the project containing dependency files.

### Code and operation

The TCP server implementation can be seen at the link: [servidor_tcp.py](https://github.com/Santos-Everton/TrabalhoPratico1/blob/main/servidor/servidor_tcp.py). 
The server creates a _socket_ to listen on a specific port passed as a parameter.
```
% servidor_tcp.py PORT
```
This is basically the only command that needs to be given to run the server.

The TCP client implementation can be seen at the link: [cliente_tcp.py](https://github.com/Santos-Everton/TrabalhoPratico1/blob/main/cliente/cliente_tcp.py).
The client connects to the server by sending the request for a file. The client side receives 5 parameters - the IP of the server, the port of the server, the execution command, the file to be requested and the file saving directory. In addition to the command to download the file, two other commands can be given, one to list the files present on the server and another to see the commands that can be given on the server by the client, as a _help_ system.
The command structure is as follows:
```
# Command to download a file
% cliente_tcp.py HOST_SERVER PORT_SERVER file NAME_FILE DESTINATION_DIRECTORY

# Command to list server files
% cliente_tcp.py HOST_SERVER PORT_SERVER list

# Command for help
% cliente_tcp.py HOST_SERVER PORT_SERVER help
```
All error handling appropriate to the problem has been done. For example: no connection to the server, file not found, invalid command.

### Considerations
The file [main.pdf](https://github.com/Santos-Everton/TrabalhoPratico1/blob/main/main.pdf) contains the specifications for the development of this project with the _plus_ requested by the teacher in the server being multi-threaded and the command to list the files of the server. In addition, a video presenting the operation of this project can be viewed at [Link do Video]().
