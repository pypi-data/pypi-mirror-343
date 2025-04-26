import socket
import netpywork

class udp_msg:
    """
    UDP Message header:

    Length 4 bytes

    Port 2 bytes

    Seq_no 4 bytes

    Seq_id 2 bytes

    Amount of ids 2 bytes

    Msg ? bytes
    """
    port:int = -1
    length: int = -1
    address: tuple = ()
    seq_no: int = -1
    seq_id: int = -1
    amount: int = -1
    data: bytes = None

class tcp_msg:
    """
    TCP Message header:

    Length 4 bytes

    Closing 1 byte

    Msg ? bytes
    """
    length:int = -1
    port:int = -1
    address: tuple = ()
    data:bytes = None
    closing:bool = False

class _utils:
    def peek_udp(sock: socket.socket,size: int):
            buffer = bytearray(size)
            # Windows workaround as it errors out with errorcode 10040 even though it peeked the msg
            try:
                sock.recv_into(buffer,size,socket.MSG_PEEK)
            except OSError as ex:
                if(ex.errno != 10040):
                    return None
            return buffer
    def read_message(byte: bytearray,length:int = -1):
        if(length == -1):
            length = len(byte)
        result = byte[0:length]
        for _ in range(length):
            del byte[0]
        return bytes(result)
    def read_udp_msg(socket: socket.socket) -> udp_msg:
        length = _utils.peek_udp(socket,4)
        # MSG Size + Size len
        length = int.from_bytes(length,"big") + 4
        result,result_address = socket.recvfrom(length)
        result = bytearray(result)
        _utils.read_message(result,4)
        port = int.from_bytes(_utils.read_message(result,2),"big")
        full_address = (result_address[0],port)
        seqno = int.from_bytes(_utils.read_message(result,4),"big")
        seqid = int.from_bytes(_utils.read_message(result,2),"big")
        amount = int.from_bytes(_utils.read_message(result,2),"big")
        result = _utils.read_message(result)
        udp_message = udp_msg()
        udp_message.address = full_address
        udp_message.data = result
        udp_message.amount = amount
        udp_message.length = length
        udp_message.port = port
        udp_message.seq_no = seqno
        udp_message.seq_id = seqid
        return udp_message
    def read_tcp_msg(socket: socket.socket):
        length = socket.recv(4)
        length = int.from_bytes(length,"big")
        buffer = socket.recv(length)
        # TCP not always reads the entire message, read byte by byte until length is correct
        while len(buffer) < length:
            buffer += socket.recv(1)
        buffer = bytearray(buffer)
        close_con = int.from_bytes(_utils.read_message(buffer,1),"big") == 1
        result = _utils.read_message(buffer)
        address = socket.getpeername()
        tcp_message = tcp_msg()
        tcp_message.address = address
        tcp_message.closing = close_con
        tcp_message.data = result
        tcp_message.length = length
        tcp_message.port = address[1]
        return tcp_message
    def send_tcp(sock: socket.socket,msg: bytes,keep_con:bool = True):
        # Length msg + 1 byte for keep con
        length = (len(msg)+1).to_bytes(4,"big")
        closing = (1 if not keep_con else 0).to_bytes(1,"big")
        sock.send(length + closing + msg)
    def send_udp(sock: socket.socket,port:int,address: tuple,msg: bytes,seq_no: int,seq_id:int ,amount:int):
        # Length msg + 2 byte for port + 4 bytes for seq + 2 bytes for seq id + 2 bytes for amount of seq
        length = (len(msg) + 2 + 4 + 2 + 2).to_bytes(4,"big")
        port = port.to_bytes(2,"big")
        seqno = seq_no.to_bytes(4,"big")
        seqid = seq_id.to_bytes(2,"big")
        amount = amount.to_bytes(2,"big")
        sock.sendto(length + port + seqno + seqid + amount + msg,address)