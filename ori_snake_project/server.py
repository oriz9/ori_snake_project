import socket
import select
import pickle

total_list = []
MAX_MSG_LENGTH = 2048
SERVER_PORT = 5555
SERVER_IP = '0.0.0.0'
LOCAL_IP = socket.gethostbyname(socket.gethostname())
print(f"Please connect you clients to: {LOCAL_IP}")


def print_client_sockets(client_sockets):
    for c in client_sockets:
        print("\t", c.getpeername())


def convert_client_to_pos_dict_to_list_of_positions(input_dict):
    total_list = []
    for x in list(input_dict.values()):
        for y in x:
            total_list.append(y)
    return total_list


print("Setting up server...")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()
print("Listening for clients...")

client_sockets = []
client_to_pos_dict = {}
while True:
    rlist, wlist, xlist = select.select([server_socket] + client_sockets, [], [], 0.1)
    for current_socket in rlist:
        if current_socket is server_socket:
            connection, client_address = current_socket.accept()
            print("New client joined!", client_address)
            client_sockets.append(connection)
            print_client_sockets(client_sockets)
        else:
            data = current_socket.recv(MAX_MSG_LENGTH)  # .decode()
            #print(data)
            if data == b'\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00C\x00\x94.':  # client disconnected!!!
                print("Connection closed", )
                client_sockets.remove(current_socket)
                current_socket.close()
                print_client_sockets(client_sockets)
                total_list = []
            else:  # client sent something
                unpickled_data = pickle.loads(data)
                client_to_pos_dict[current_socket] = unpickled_data
                # ((sock1, messahe_to_sock1), (sock2, message_to_sock2)...)a

    msg_to_send = convert_client_to_pos_dict_to_list_of_positions(client_to_pos_dict)
    msg_after_pickle = pickle.dumps(msg_to_send)
    for temp_client_socket in client_sockets:
        temp_client_socket.send(msg_after_pickle)