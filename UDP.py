import time
import socket
def udp_recv(client_socket):
    print("Server is waiting for a connection...")

    # Receiving data from the server
    data, addr = client_socket.recvfrom(1024) # Using recvfrom method

    print(f"Received message: {data} from {addr}")
    
    # Send an acknowledgment back to the server
    client_socket.sendto(b'ACK', addr) # Using sendto method
    return [data,addr]
     

        
def udp_send(message, port):
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set a timeout for the response (2 seconds)
    client_socket.settimeout(2)

    try:
        # Send the message to the server
        client_socket.sendto(message.encode('utf-8'), ('localhost', port))
        
        # Wait for the acknowledgment from the server
        data, addr = client_socket.recvfrom(1024)

        print(f"Received acknowledgment: {data.decode()} from {addr}")
    except socket.timeout:
        print("Packet was lost, resending...")
        udp_send(message, port)
    finally:
        client_socket.close()
