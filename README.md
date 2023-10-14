# Protocol
## Handshake
![handshake](./Images/handshake.png)

### Packets
#### From client to server
##### New group request
```
0               1               2               3               4
0 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Type (0x01)  |      Port     | Interval (us) |  Members cnt  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|M. IPv4|  ...  |
+-+-+-+-+-+-+-+-+
```

##### Create group OK/NOK
```
0               1               2  
0 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Type (0x02)  |F|    Movie ID   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

##### Enter group request
```
0               1               2               3               4 
0 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Type (0x04)  |      Port     |    Group ID   | Interval (us) |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

##### Enter group OK/NOK
```
0               1  
0 1 2 3 4 5 6 7 8 1
+-+-+-+-+-+-+-+-+-+
|   Type (0x08) |F|
+-+-+-+-+-+-+-+-+-+
```

#### From server to client
##### New group received
```
0               1               2               3               4
0 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Type (0x10)  |      Port     |    Group ID   |   Movie cnt   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|    Movie ID   |  M. name size |   Movie name  |      ...      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

##### Enter group received
```
0               1               2
0 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Type (0x20)  |      Port     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

##### Group Created
```
0               1               2               3               4
0 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Type (0x40)    | Interval (us) |  Members cnt  |M. IPv4|  ...  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

#### Fields
| Field | Meaning |
|;------ | ;------- |
| [Type](#type) | Type of packet |
| [Port](#port) | Port that will be used to communicate |
| [Interval](#interval) | Time interval between stream packets |
| [Members cnt](#members) | How many members will join the group |
| [Member IPv4](#members) | IPv4 address of member |
| [Movie ID](#movie) | Indicates the ID of a movie |
| [Group ID](#groups-id) | Indicates the ID of a group |
| [M. name size](#movie) | Indicates the length of the movie name in bytes |
| [Movie name](#movie) | Name of the movie |
| [F](#flag) | Flag to indicate wheter the client could connect to the server |
| ... | In packets with variable size, the dots represents the remaining elements |

##### Type
Each message has a type to indicate the operation type and each type is a power of
two. The flags and it's values are listed in the table below:

| Type | Packet |
| ;--- | ;------ |
| 0x01 | [New group request](#new-group-request) |
| 0x02 | [Create group ok/nok](#create-group-ok/nok) |
| 0x04 | [Enter group request](#enter-group-request) |
| 0x08 | [Enter group ok/nok](#enter-group-ok/nok) |
| 0x10 | [New group received](#new-group-received) |
| 0x20 | [Enter group received](#enter-group-received) |
| 0x40 | [Group created](#group-created) |

##### Port
During the negotiation phase, the port field is used to determine which port
will be used in communication by both the server and the client. After
succesfully binding to a commom port, the communication between the server and
the client will occur through it. The server will send it's packets throgh the
new port and expect new packets from the client to arrive though the new port. 
The client will close the socket to the standart port.

##### Interval
A interval time in microseconds between stream packets can be set, both the server 
and the clients can set a interval time. During handshake it's value will be 
choosen by taking the biggest value set by the server and the clients in the 
trasmission group.

##### Members
Each group has a set of members that are identified by it's IPv4 addressess.
During handshake the leader member (the one to initiate the handshake process),
will send the amount of members that are expected to join and the IPv4 address
of each member.

##### Movie
Each movie is represented by a ID. During handshake the movie is choosen by the
leader member.

##### Flag
A the end of the handshake, the flag field indicates wheter the client could
connect to the same port as the server.

## Server
## Client
## Stream
## Sockets
## Log
## Watchdog
