import os
import shutil
import pkg_resources


def copy_directory_contents(src_dir, dest_dir):
    """
    复制源目录中的所有文件到目标目录
    """
    # 确保目标目录存在
    os.makedirs(dest_dir, exist_ok=True)

    # 获取源目录中的所有文件
    try:
        files = pkg_resources.resource_listdir('unisound_agent_frame', src_dir)
        for file in files:
            src_file = pkg_resources.resource_filename('unisound_agent_frame', os.path.join(src_dir, file))
            dest_file = os.path.join(dest_dir, file)

            if os.path.isfile(src_file):
                shutil.copy2(src_file, dest_file)
                print(f"Copied {file} to {dest_dir}")
    except Exception as e:
        print(f"Error while copying files from {src_dir}: {str(e)}")


def check_requirements():
    """
    检查并更新requirements.txt文件
    """
    current_dir = os.getcwd()
    requirements_file = os.path.join(current_dir, 'requirements.txt')

    # 如果文件不存在，创建一个空文件
    if not os.path.exists(requirements_file):
        open(requirements_file, 'w').close()
        print(f"Created new requirements.txt file at {current_dir}")

    # 读取现有内容
    with open(requirements_file, 'r') as f:
        requirements = f.read().splitlines()

    # 检查是否已包含unisound-agent-frame
    if 'unisound-agent-frame' not in requirements:
        with open(requirements_file, 'a') as f:
            f.write('\nunisound-agent-frame')
        print("Added unisound-agent-frame to requirements.txt")


def init():
    """
    初始化命令，复制 template 和 scripts 目录下的文件到目标位置
    """
    current_dir = os.getcwd()

    # 复制 template 目录内容到 config 目录
    config_dir = os.path.join(current_dir, 'config')
    copy_directory_contents('template', config_dir)

    # 复制 scripts 目录内容
    scripts_dir = os.path.join(current_dir, 'scripts')
    copy_directory_contents('scripts', scripts_dir)

    # 复制 service.py 文件到根目录
    try:
        service_src = pkg_resources.resource_filename('unisound_agent_frame', 'service.py')
        service_dest = os.path.join(current_dir, 'service.py')
        shutil.copy2(service_src, service_dest)
        print(f"Copied service.py to {current_dir}")
    except Exception as e:
        print(f"Error while copying service.py: {str(e)}")

    # 检查并更新requirements.txt
    check_requirements()

    print("\nInitialization completed successfully!")
    print(f"- Template files copied to: {config_dir}")
    print(f"- Script files copied to: {scripts_dir}")
    print(f"- Service file copied to: {current_dir}")
    print(f"- Requirements file updated at: {current_dir}")
