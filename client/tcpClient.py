import socket


def client_conn(host, port):
    # 先建立连接
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    return client

# def down_load(filesize,filename):
#     recv_size = 0
#     print('----->', filename)
#     with open(filename, 'wb') as f:
#         while recv_size < filesize:
#             recv_data = client.recv(1024)
#             f.write(recv_data)
#             recv_size += len(recv_data)
#             print('recvsize:%s filesize:%s' % (recv_size, filesize))
#     print('%s :下载成功'%filename)
#
#
#
#
#
# def get_file():
#     if not user_info['name']:
#         print('请先登录')
#         return
#     while True:
#         send_dic = {'type': 'get_list', 'name': user_info['name']}
#         back_dic = send_data(send_dic, None)
#         if back_dic['flag']:
#             for i,file in enumerate(back_dic['file_list']):
#                 print('%s:%s'%(i,file))
#             choose=input('请输入要下载的影片：').strip()
#             if choose.isdigit():
#                 down_dic={'type':'download','file_name':back_dic['file_list'][choose],'session':user_info['session']}
#                 back_down=send_data(down_dic)
#                 down_load(back_down['file_size'],back_down['file_name'])
#                 break
#             else:
#                 print('请输入数字')
#
#         else:
#             print(back_dic['msg'])
