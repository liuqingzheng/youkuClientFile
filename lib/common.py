import struct
import json
import os


def send_data(client, send_dic, file):
    # 发送部分
    head_json_bytes = json.dumps(send_dic).encode('utf-8')  # 先把报头转为bytes格式
    client.send(struct.pack('i', len(head_json_bytes)))  # 先发报头的长度
    client.send(head_json_bytes)  # 再发送报头
    if file:  # 如果存在文件，再把文件打开一行一行发送
        with open(file, 'rb') as f:
            for line in f:
                client.send(line)
    # 接收部分
    back_len_bytes = client.recv(4)  # 先收报头4个bytes,得到报头长度的字节格式
    back_head_len = struct.unpack('i', back_len_bytes)[0]  # 提取报头的长度
    # recv_size = 0
    # head_bytes = b''
    # while recv_size < back_head_len:
    #     recv_data = client.recv(1024)
    #     recv_size += len(recv_data)
    #     head_bytes = head_bytes + recv_data

    head_bytes = client.recv(back_head_len)  # 按照报头长度back_head_len,收取报头的bytes格式
    header = json.loads(head_bytes.decode('utf-8'))  # 把bytes格式的报头，转换为json格式

    return header


def get_allfile_by_path(path):
    file_list = os.listdir(path)
    return file_list
