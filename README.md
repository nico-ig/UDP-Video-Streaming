# Protocol
This protocol aims to describe a method to concurrently streaming different movies
to different groups of clients. To do so, it has two mais phases: the 
[handshake](#handshake) phase and the [streaming](#streaming) phase. In the handshake 
phase, it allocates a port between a leader client and the server. 
In the streaming phase, the clients wishing to join register to that session 
and the leader client chooses a available movie from the server to be streamed.
When the movie has finished being streamed, the session is closed.

## Handshake
![handshake](./images/port-negotiation.png)

### Packets
#### Fields
#### From client to server
#### From server to client

## Streaming
### Registration
![registration](./images/registration.png)

### Movie selection
![movie selection](./images/movie-selection.png)

### Movie stream

## Limitations
* The protocol doesn't define any protection against attacks to the server or to 
the client by overloading them with requests/responses.
* It also doesn't ensure that all members could connect to the server before
  starting to stream.
* After a stream has started, no other member can join, neither the stream can be
  paused.
* When a client loses connection to the server, the other clients in the group
  are not notified.
* The port is negotiated only with the leader, other clients in the same stream
  won't be able to watch it if they are using that port for something else,

# Implementation
## Modules
### Server
![server](./images/server.png)

### Client
![client](./images/client.png)

### Handshake
#### Server
![server handshake](./images/handshake-server.png)

#### Client
![client handshake](./images/handshake-client.png)

To avoid trying to connect indefinitly to the server, the client has a limit to
the number of attempts to try to establish the handshake.

### Stream
The interval between stream packets has a maximum and minimum thresholds.

### Sockets
### Watchdog
### Log
### Statistics

## Tests
## Project structure
Estrutura de arquivos:
```
/ 
|-----main.py 
|-----/tests
|-----/images
|-----/movies
|-----/server
|       |-----main.py
|       |-----parses.py
|       |-----handshake.py
|       |-----streaming.py
|       |-----registration.py
|
|-----/client
|       |-----main.py
|       |-----parses.py
|       |-----handshake.py
|       |-----streaming.py
|       |-----registration.py
|
|-----/utils
        |-----log.py
        |-----watchdog.py
        |-----statistics.py
```

