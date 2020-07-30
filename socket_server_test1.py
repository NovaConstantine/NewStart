import socket



host = '172.24.11.241'

port = 502
web = socket.socket()
web.bind((host,port))
web.listen(2)
print('开启循环')
while True:
    conn,addr = web.accept()

    data = conn.recv(1024)

    print(data.decode('utf-8'))
    conn.sendall(bytes('Http 1.1 200 ok \n\n Hello World!'.encode('utf-8')))

    conn.close()

    
