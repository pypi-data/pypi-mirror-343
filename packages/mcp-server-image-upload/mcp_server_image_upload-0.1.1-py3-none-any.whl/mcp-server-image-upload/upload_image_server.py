import os
import paramiko
import argparse

from mcp.server.fastmcp import FastMCP


# 初始化 MCP 服务器
mcp = FastMCP("UploadImageSever")
USER_AGENT = "UploadImageSever-app/0.1.1"

# 全局变量用于存储远程连接参数
g_remote_ip = None
g_remote_username = None
g_remote_save_path = None
g_remote_password = None

@mcp.tool()
def upload_image(local_path):
    """
    当用户涉及到图片上传或者用户拖拽图片到当前窗口，应记录当前图片路径，并结合传入的参数调用本函数，
    即使用 SFTP 将本地图像文件上传到远程服务器。或者当某个用具需要使用图片但又无图片可用时，用户输入图片
    路径或者图片，也可以使用本函数进行上传。
    参数:
        local_path (str): 本地图像文件的路径。
    返回:
        str: 如果成功，则为文件在远程服务器上的完整路径；如果发生错误，则为描述错误的字符串。
    """
    if not os.path.exists(local_path):
        error_msg = f"Error: Local file not found: {local_path}"
        print(error_msg)
        return error_msg

    if not g_remote_password:
        error_msg = "Error: Password must be provided for authentication."
        print(error_msg)
        return error_msg

    transport = None
    sftp = None
    try:
        # 建立 SSH 连接
        transport = paramiko.Transport((g_remote_ip, 22))  # 默认 SFTP 端口是 22
        transport.connect(username=g_remote_username, password=g_remote_password)

        # 打开 SFTP 会话
        sftp = paramiko.SFTPClient.from_transport(transport)

        # 拼接完整的远程路径
        local_filename = os.path.basename(local_path)
        remote_path = os.path.join(g_remote_save_path, local_filename).replace('\\', '/') # 确保使用正斜杠

        # 确保远程目录存在（可选，如果需要则创建）
        try:
            sftp.stat(os.path.dirname(remote_path))
        except FileNotFoundError:
            dirs = []
            curr_dir = os.path.dirname(remote_path)
            while True:
                try:
                    sftp.stat(curr_dir)
                    break
                except FileNotFoundError:
                    dirs.append(os.path.basename(curr_dir))
                    curr_dir = os.path.dirname(curr_dir)
                    if not curr_dir or curr_dir == '/':
                        break
            for i in range(len(dirs) - 1, -1, -1):
                curr_dir = os.path.join(curr_dir, dirs[i])
                sftp.mkdir(curr_dir)

        # 上传文件
        sftp.put(local_path, remote_path)
        print(f"Successfully uploaded {local_path} to {g_remote_ip}:{remote_path}")
        return remote_path

    except paramiko.AuthenticationException as e:
        error_msg = f"Error: Authentication failed: {e}"
        print(error_msg)
        return error_msg
    except paramiko.SSHException as e:
        error_msg = f"Error: SSH connection error: {e}"
        print(error_msg)
        return error_msg
    except IOError as e:
        error_msg = f"Error: File transfer error: {e}"
        print(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Error: An unexpected error occurred: {e}"
        print(error_msg)
        return error_msg
    finally:
        if sftp:
            sftp.close()
        if transport:
            transport.close()


def main():
    global g_remote_ip, g_remote_username, g_remote_save_path, g_remote_password
    parser = argparse.ArgumentParser(description="upload image server")
    parser.add_argument("--remote_ip", type=str, required=True, help="上传图片的机器的IP")
    parser.add_argument("--remote_username", type=str, required=True, help="上传图片的机器的用户名")
    parser.add_argument("--remote_save_path", type=str, required=True, help="上传图片的机器的所在路径")
    parser.add_argument("--remote_password", type=str, required=True, help="与用户名配对的密码")
    args = parser.parse_args()

    # 将参数赋值给全局变量
    g_remote_ip = args.remote_ip
    g_remote_username = args.remote_username
    g_remote_save_path = args.remote_save_path
    g_remote_password = args.remote_password

    # upload_image(local_path=LOCAL_IMAGE_PATH)

    # 以标准 I/O 方式运行 MCP 服务器
    mcp.run(transport='stdio')


if __name__ == '__main__':
    main()