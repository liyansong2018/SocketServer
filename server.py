import socket
import threading
import os
 

def sending_file(connection):
    try:
        # 接收消息头
        # file_info_size = struct.calcsize('128sl')
 
        head = connection.recv(1024)
 
        if head:
            data = head.decode("utf-8").split(";")
            file_name = data[1][9:]
            file_size = data[0][15:]
 
            file_new_dir = os.path.join('receive')
            if not os.path.exists(file_new_dir):
                os.makedirs(file_new_dir)
 
            file_new_name = os.path.join(file_new_dir, file_name)
            received_size = 0
            # 如果文件已存在
            if os.path.exists(file_new_name):
                received_size = os.path.getsize(file_new_name)
            
            # 发送文件大小
            connection.send((str(received_size) + "\n").encode("utf-8"))
            print((str(received_size) + "\n").encode("utf-8"))
            print("start receiving file:", file_name)

            write_file = open(file_new_name, 'ab')
            while not str(received_size) == file_size:
 
                receive_origin = connection.recv(40960)
                if receive_origin == b"break...":
                    break
                receive_data = receive_origin
                received_size += len(receive_data)
                print(received_size)
                write_file.write(receive_data)

            if str(received_size) == file_size:
                print("接收完成！\n")
            else:
                print("接收暂停！")
            write_file.close()

        connection.close()
 
    except Exception as e:
        print(e)
 
 
if __name__ == '__main__':
    host = socket.gethostname()
 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("192.168.42.166", 8888))
    print("服务已启动---------------")
    sock.listen(2)
    address = sock.accept()[1]
    print("客户端已连接：", address)

    fileSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fileSocket.bind(("192.168.42.166", 9999))
    fileSocket.listen(5)

    while True:
        connection, address = fileSocket.accept()
        print("发送文件的客户端地址：", address)
        thread = threading.Thread(target=sending_file, args=(connection,))
        thread.start()
