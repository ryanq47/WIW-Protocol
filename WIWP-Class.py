## this could all be a class eventually, but for now, it's on its own

import socket
import math
import time


## ToDO;

## Error handling
## Proper Logging

class WIWP:
    
    def __init__(self, IP, PORT):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # this allows the socket to be reelased immediatly on crash/exit
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.ip = IP
        self.port = int(PORT)
        
    def bind_and_listen(self):
        self.server.bind((self.ip, self.port))
        print("LISTENING")
        self.server.listen()
        print("ACCEPTING")
        self.conn, self.addr = self.server.accept()
    
    def connect(self):
        try:
            self.server.connect((self.ip, self.port))
        
        except Exception as e:
            print(e)

    ##===============================Recv Protocol==================================================
    """
        

    Protocol order/steps/Definitions:

    HEADER_BYTES: The size of the header. Currently 10 bytes, this allows for a theoretical 1.17 yottabytes to be transfered before the protocol limits out. 
                (That number is quite ridiculous, so the other header space may get used for other items in the future)

    Header: The header contains the size of the message to be sent. I.E: If your message was 1024 Bytes, the header will contain '1024'

    Chunk: A partial piece of the entire message. Each chunk is equal to the size of the buffer. 

    1) Listen for header.

    2) Calculate chunk size based on header

    3) Recieve the remaining chunks based on the header size

    4) (optional/based on code flow): Return data to calling function, and/or loop

        
    """

    def recieve_msg(self):
        ## lazy re-assignemnt
        conn = self.conn        
        complete_msg = ""
        
        new_msg = True
        
        ## clients need to have a shared known header beforehand. Default is 10
        HEADER_BYTES = 10
        BUFFER = 1024
        header_value = 0
        header_contents = ""
        
        msg_bytes_recieved_so_far = 0
        
        print(f"WAITING ON HEADER TO BE SENT:")
        header_msg_length = conn.recv(HEADER_BYTES).decode() #int(bytes_decode(msg)
        print("HEADER:" + header_msg_length)
        
        ## getting the amount of chunks/iterations eneded at 1024 bytes a message
        chunks = math.ceil(int(header_msg_length)/BUFFER)
        #print(chunks)
        
        #print(bytes_decode(msg))
        
        complete_msg = "" #bytes_decode(msg)[10:]
        
        #while True:
        for i in range(0, chunks):
            print(f"RECEVING CHUNK:")
            msg = conn.recv(BUFFER)  # << adjustble, how many bytes you want to get per iteration
            
            ## getting the amount of bytes sent so far
            msg_bytes_recieved_so_far = msg_bytes_recieved_so_far + len(self.bytes_decode(msg))

            
            complete_msg += self.bytes_decode(msg)
            
            print(self.bytes_decode(msg))
            
            print(f"""DEBUG:
                Full Message Length (based on header value) {header_msg_length}
                Header size: {HEADER_BYTES}

                Size of message recieved so far: {msg_bytes_recieved_so_far}  
                
                Chunks: {chunks}          
                
                """)
            
            ## if complete_msg is the same length as what the headers says, consider it complete. 
            if len(complete_msg) == header_msg_length:
                print("MSG TRANSFER COMPLETE")
        
        print("VALUE OF MSG: \n" + complete_msg)
        return complete_msg

    ##===============================Send Protocol==================================================
    """
        
    Protocol order/steps/Definitions:

    HEADER_BYTES: The size of the header. Currently 10 bytes, this allows for a theoretical 1.17 yottabytes to be transfered before the protocol limits out. 
                (That number is quite ridiculous, so the other header space may get used for other items in the future)

    Header: The header contains the size of the message to be sent. I.E: If your message was 1024 Bytes, the header will contain '1024'

    Chunk: A partial piece of the entire message. Each chunk is equal to the size of the buffer. 

    1) Connect to listening server

    2) Send the header

    3) Calculate chunk size based on header

    4) Send the chunks based on the header size


        
    """           

    def send_msg(self, msg="TestMessage"):
        #msg = str_encode(_msg)
        
        ##lazy re-assignment
        conn = self.server
        ## clients need to have a shared known header beforehand. Default is 10
        HEADER_BYTES = 10
        BUFFER = 1024
        
        ## get the length of the message in bytes
        msg_length = len(msg)
        
        ## create a header for the message that includes the length of the message
        header = self.str_encode(str(msg_length).zfill(HEADER_BYTES))#.encode()
        
        ## send the header followed by the message in chunks
        print(f"SENDING HEADER: {header}")
        conn.send(header)
        
        for i in range(0, math.ceil(msg_length/BUFFER)):
            
            ## gets the right spot in the message in a loop
            chunk = msg[i*BUFFER:(i+1)*BUFFER]
            print(f"SENDING CHUNK: {chunk}")
            conn.send(self.str_encode(chunk))
            

    def bytes_decode(self, input) -> str:
        decoded_result = input.decode()
        return decoded_result

        ## str -> bytes
    def str_encode(self, input) -> bytes:
        encoded_result = input.encode()
        return encoded_result

'''
## Server Code

if __name__ == "__main__":
    server = WIWP(IP,PORT)
    server.bind_and_listen()
    server.receive_msg()


'''


'''
##client code

if __name__ == "__main__":
    IP,PORT = "127.0.0.1", 80
    server = WIWP(IP,PORT)
    server.connect()
    server.send_msg()
'''
