import paramiko

ip_robot = "10.0.7.63"
port_trans = 22

c_path = "E:/work/CNLP/resource/test.wav"
r_path = "/home/nao/test.wav"

#文件在本机与nao机器人间传递测试
def transit():
    transport = paramiko.Transport((ip_robot, port_trans))
    print ("test1")
    transport.connect(username="nao", password="nao")
    print ("test2")
    sftp = paramiko.SFTPClient.from_transport(transport)
    print ("test3")
    sftp.get(r_path, c_path)
    print ("test4")

    sftp.close()
    transport.close()


if (
        __name__ == "__main__"):
    transit()