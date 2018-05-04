from client import tcpClient
from lib import common
from conf import setting
import os

admin_data = {
    'session': None,
    'name': None
}

send_dic = {'type': None, 'user_type': 'admin', 'name': None, 'session': None}


def admin_register(client):
    print('管理员注册')
    while True:
        name = input('请输入手机号>>:').strip()
        password = input('请输入密码>>').strip()
        conf_password = input('请确认密码>>:').strip()
        if password == conf_password:
            send_dic = {'type': 'register', 'user_type': 'admin', 'name': name, 'password': password}
            back_dic = common.send_data(client, send_dic, None)
            if back_dic['flag']:
                print(back_dic['msg'])
                break
            else:
                print(back_dic['msg'])

        else:
            print('两次密码不一致')


def admin_login(client):
    print('管理员登录')
    while True:
        name = input('用户名>>').strip()
        if name == 'q': break
        password = input('密码>>').strip()
        send_dic = {'type': 'login', 'user_type': 'admin', 'name': name, 'password': password}

        back_dic = common.send_data(client, send_dic, None)
        if back_dic['flag']:
            admin_data['name'] = name
            admin_data['session'] = back_dic['session']
            print(back_dic['msg'])
            break
        else:
            print(back_dic['msg'])


def upload_movie(client):
    if not admin_data['name']:
        print('请先登录')
        return
    print('上传视频')
    while True:
        up_list = common.get_allfile_by_path(setting.BASE_MOVIE_UP)
        if not up_list:
            print('暂无能上传的影片')
            break
        for i, m in enumerate(up_list):
            print('%s : %s' % (i, m))
        choose = input('请选择要上传的影片').strip()
        if choose.isdigit():
            choose = int(choose)
            need_fee = input('是否收费（y/n）>>:').strip()
            if need_fee == 'y':
                is_free = 0
            else:
                is_free = 1
            movie_path = os.path.join(setting.BASE_MOVIE_UP, up_list[choose])
            fsize = os.path.getsize(movie_path)
            send_dic = {'type': 'upload', 'user_type': 'admin', 'name': admin_data['name'],
                        'session': admin_data['session'],
                        'file_name': up_list[choose], 'file_size': fsize, 'is_free': is_free}
            back_dic = common.send_data(client, send_dic, movie_path)
            if back_dic['flag']:
                print(back_dic['msg'])
                break
            else:
                print(back_dic['msg'])

        else:
            print('请输入数字')


def delete_movie(client):
    '''
    1 先拿到视频列表，打印
    2 根据视频前数字，选择要删除的视频
    3 删除成功/失败，打印
    '''
    if not admin_data['name']:
        print('请先登录')
        return
    print('删除视频')
    while True:
        send_dic['type'] = 'get_movie_list'
        send_dic['name'] = admin_data['name']
        send_dic['session'] = admin_data['session']
        back_dic = common.send_data(client, send_dic, None)
        if back_dic['flag']:
            for i, mo in enumerate(back_dic['movie_list']):
                print('%s : %s--%s' % (i, mo[0], mo[1]))
            choose = input('请输入要删除的电影（数字）：').strip()
            if choose.isdigit():
                choose = int(choose)
                send_dic['type'] = 'delete_movie'
                send_dic['movie_name'] = back_dic['movie_list'][choose][0]
                back_dic = common.send_data(client, send_dic, None)
                if back_dic['flag']:
                    print(back_dic['msg'])
                    break
                else:
                    print(back_dic['msg'])

            else:
                print('请输入数字')

        else:
            print(back_dic['msg'])
            break


def release_notice(client):
    if not admin_data['name']:
        print('请先登录')
        return
    print('发布公告')
    while True:
        notice_name = input('请输入公告标题：').strip()
        notice_content = input('请输入公告内容').strip()
        send_dic['type'] = 'release_notice'
        send_dic['name'] = admin_data['name']
        send_dic['session'] = admin_data['session']
        send_dic['notice_name'] = notice_name
        send_dic['notice_content'] = notice_content
        back_dic = common.send_data(client, send_dic, None)
        if back_dic['flag']:
            print(back_dic['msg'])
            break
        else:
            print(back_dic['msg'])


fun_dic = {
    '1': admin_register,
    '2': admin_login,
    '3': upload_movie,
    '4': delete_movie,
    '5': release_notice,
}


def admin_view():
    client = tcpClient.client_conn('127.0.0.1', 8081)
    while True:
        print('''
        1 注册
        2 登录
        3 上传视频
        4 删除视频
        5 发布公告
        ''')

        choose = input('please choose>>:').strip()
        if 'q' == choose: break
        if choose not in fun_dic: continue
        fun_dic[choose](client)
    client.close()
