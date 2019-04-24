import socket

HOST_NAME ,PORT_NUMBER = '127.0.0.1' , 8080

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def server_start():
    try:
        print("Starting server on..... " + str(HOST_NAME) + ":" + str(PORT_NUMBER))
        listen_socket.bind((HOST_NAME,PORT_NUMBER))
        print("Started server on....")
        server_conn()

    except OSError:
        print(" port is already in use ")
        server_shutdown()
    except IndexError:
        print(" port is already in use ")
        server_shutdown()
    
       

def server_shutdown():
    try:
        print("Server shutting down.....")
        listen_socket.shutdown(socket.SHUT_RDWR)  
    except Exception:
        pass



def define_headers(file_code, file_type):
    print("Requested File Type : " + file_type)

    header = ''
    if file_code == 500:
        header += 'HTTP/1.1 500 Unexpected error\n'
    elif file_code == 200:
        header +=  'HTTP/1.1 200 OK\n'
    elif file_code == 403:
        header += 'HTTP/1.1 403 Access denied\n'
    elif file_code == 400:
        header += 'HTTP/1.1 400 Bad Request\n'

    if file_type == 'jpg' or file_type == 'jpeg': 
        header += 'Content-Type: image/jpeg\n'
    elif file_type == 'html' or file_type == 'php':
        header += 'Content-Type: text/html\n'
    elif file_type == 'png':
        header += 'Content-Type: image/png\n'
    elif file_type == 'css':
        header += 'Content-Type: text/css\n'
    

    header += 'Connection: close\n\n'
    return header

def server_conn():
    listen_socket.listen()
    while True:
        (client_connection,client_address) = listen_socket.accept()
        client_connection.settimeout(120)
        
           
        while True:
            request=client_connection.recv(1024).decode()
            print (request)
        
            file_requested = request.split(' ')[1]
            file_requested = file_requested.split('?')[0]

            if file_requested == "/":
                file_requested = "/index.html"

            file_path = 'server' + file_requested

            try:
                response_header = "HTTP/1.1 200 OK\n\n"
                response_header = response_header.encode()
                f = open(file_path, 'rb')
                response_data = f.read()
                f.close()
               
            
                print("Requested File : " + file_path)

            except FileNotFoundError:
                response_header = b"HTTP/1.1 404 Not Found\n\n"
                response_data = b"<h1>Error 404 - File Not Found<h1>"
            except UnboundLocalError as e:  
                response_header = b"HTTP/UnboundlocalError\n\n"
                response_data = b"<h1>unbound error request<h1>"
            except IndexError as e:  
                response_header = b"HTTP/IndexError\n\n"
                response_data =b"<h1>Index error<h1>"
            except SystemError as e:  
                response_header = b"HTTP/SystemError\n\n"
                response_data =b"<h1>SystemError<h1>"
                   
                response_header += b'connection: close\n\n'
            
            print(response_header.decode())
            response = response_header + response_data
    
            client_connection.send(response)
            client_connection.close()
            break


server_start()

        

  







    


        
