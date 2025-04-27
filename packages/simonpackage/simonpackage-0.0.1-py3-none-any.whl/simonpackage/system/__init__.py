import os
import time

import pyperclip
from apscheduler.schedulers.blocking import BlockingScheduler


def setScheduled(func, args=(), trigger='interval', **kwargs):
    """
    set next_run_time=datetime.datetime.now() has the effect of running the job once immediately
    scheduler.add_job(func=print_time, args=('任务只执行一次，在下一次的时间执行',),
                  next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=60))

scheduler.add_job(func=print_time, args=('时间打印定时任务',), trigger='interval', seconds=5)  # 每5秒执行一次
scheduler.add_job(func=print_time, args=('时间打印定时任务',), trigger='interval', minutes=2)  # 每2分钟执行一次
scheduler.add_job(func=print_time, args=('时间打印定时任务',), trigger='interval', hours=1)  # 每1小时执行一次

scheduler.add_job(func=print_time, args=('时间打印定时任务',), trigger='cron', minute='*', second='1')  # 每分钟执行一次
scheduler.add_job(func=print_time, args=('时间打印定时任务',), trigger='cron', hour='*', minute='0',
                  second='0')  # 每小时执行一次

scheduler.add_job(func=print_time, args=('时间打印定时任务',), trigger='cron', hour='20', minute='0',
                  second='0')  # 每天20:00执行一次
scheduler.add_job(func=print_time, args=('时间打印定时任务',), trigger='cron', hour='21')  # 每天21:00执行一次"""
    scheduler = BlockingScheduler()
    scheduler.add_job(func, args=args, trigger=trigger, **kwargs)
    scheduler.start()


def auto_deb_pack(project=None, show_terminal=False, maintainer='Simon Zhang', architecture='arm64', version="1.0.0",
                  description='a small tool',
                  repack=True, cleanup=True, root_password='1', dependent_packages=None, copy_data_list=None):
    """
    :param project: the name of the project and also the name of the main file, if not specified, will be the folder name
    :param show_terminal: whether to show the console when running the programme
    :param maintainer:
    :param version:
    :param description:
    :param repack: whether to rebuild the binary file using pyinstaller
    :param cleanup: whether to clean up the temporary directories and files
    :param copy_data_list:list of additional files or folders that need to be copied to the project directory
    :return:
    """
    if project is None:
        project = os.path.abspath(os.curdir).rsplit('/')[-1]
        print(project)

    if repack:
        os.system(f'pyinstaller -y -w -i res/{project}.ico {project}.py')
        os.system(f'cp ./res -R ./dist/{project}/')
    if copy_data_list is not None:
        for data in copy_data_list:
            if os.path.exists(data):
                os.system(f'cp {data} -R ./dist/{project}/')  # works with folder OR file
    if dependent_packages is not None:
        package_list = f"({' '.join(dependent_packages)})"
    else:
        package_list = ''
    project_deb = f'{project}_deb'
    user_name = os.getlogin()
    DEBIAN_path = f'./{project_deb}/DEBIAN'
    application_path = f'./{project_deb}/usr/share/applications'
    icons_path = f'./{project_deb}/usr/share/icons'
    lib_project_path = f'./{project_deb}/usr/lib/{project}'
    res_dir = f'{lib_project_path}/res'

    # 图标文件
    project_icon = ''
    if os.path.exists(f'{project}.ico'):
        project_icon = f'{project}.ico'
    elif os.path.exists(f'{project}.svg'):
        project_icon = f'{project}.svg'
    elif os.path.exists(f'{project}.png'):
        project_icon = f'{project}.png'
    elif os.path.exists(f'{project}.bmp'):
        project_icon = f'{project}.bmp'
    # control terminal showing
    terminal = 'true' if show_terminal else 'false'

    os.makedirs(DEBIAN_path, exist_ok=True)
    os.makedirs(icons_path, exist_ok=True)
    os.makedirs(application_path, exist_ok=True)
    os.makedirs(lib_project_path, exist_ok=True)

    control = f'''Package: {project}
Version: {version}
Architecture: {architecture}
Maintainer: {maintainer}
Description: {description}
'''
    # 写上sudo在运行进需要管理员权限，但是仍算是用户目录下，而不是根目录
    postinst = f"""#! /bin/bash
echo "initialize the environment necessary"
echo {root_password} | sudo cp /usr/share/applications/{project}.desktop ~/Desktop
echo {root_password} | sudo mkdir -p res
echo {root_password} | sudo cp -R /usr/lib/{project}/res/ ~/res
packages={package_list}
for app in ${{packages[@]}};do
    echo {root_password} | sudo apt install ${{app}}
    sleep 5
done
echo "all needed files are installed correctly"

sleep 5

echo POST INSTALLATION FUNCTION EXECUTED
"""

    desktop = f"""[Desktop Entry]
Categories=Office
Comment={description}
Exec=/usr/lib/{project}/{project}
Icon=/usr/share/icons/{project_icon}
Name={project}
Terminal={terminal}
Type=Application
X-Deepin-Vendor=user-custom
X-Ubuntu-Touch=true
"""

    with open(f'{DEBIAN_path}/control', 'w', encoding='utf8') as f:
        f.write(control)

    with open(f'{DEBIAN_path}/postinst', 'w', encoding='utf8') as f:
        f.write(postinst)

    with open(f'{application_path}/{project}.desktop', 'w', encoding='utf8') as f:
        f.write(desktop)

    if os.path.exists('res'):
        os.system(f'cp -R ./res {lib_project_path}')
        os.system(f'cp res/{project_icon} {icons_path}')
    elif os.path.exists(f'{project_icon}'):
        os.system(f'cp {project_icon} {icons_path}')

    src_dir = f'./dist/{project}'
    dst_dir = f'./{project_deb}/usr/lib'
    os.system(f'chmod 775 {DEBIAN_path}/postinst')
    os.system(f'cp -R {src_dir} {dst_dir}')
    time.sleep(5)
    os.system(f'dpkg -b {project_deb} {project}_{version}_arm64.deb')
    if cleanup:
        os.system(f'rm -R build')
        os.system(f'rm -R dist')
        os.system(f'rm -R {project_deb}')
        os.system(f'rm {project}.spec')
    os.system(f'echo {root_password} | sudo -S dpkg -i {project}_{version}_arm64.deb')


def auto_deb_pack_qt(project=None, show_terminal=False, maintainer='Simon Zhang', architecture='arm64', version="1.0.0",
                     description='a small tool',
                     cleanup=False, root_password='1', dependent_packages=None, copy_data_list=None):
    """
    build deb packages for qt projects, the name need to be all lowercased letters and numbers, none else.
    first need to make release version.
    :param project: the name of the project and also the name of the main file. default to current diretory
    :param architecture: the architecture type of the system, like amd64, or arm64
    :param root_password:
    :param dependent_packages: dependency apt packages that need to be installed
    :param show_terminal: whether to show the console when running the programme
    :param maintainer:
    :param version:
    :param description:
    :param cleanup: whether to clean up the temporary directories and files
    :param copy_data_list:list of additional files or folders that need to be copied to the project directory
    :return:
    """
    if project is None:
        project = os.path.abspath(os.curdir).rsplit('/')[-1]
        print(project)

    dist_folder = f'build-{project}-ex-Release'
    # 将release文件夹内容复制到工程目录
    os.system(f'cp -R ../{dist_folder} .')

    # 复制动态链接库文件

    copy_command = f"""deplist=$(ldd ./{dist_folder}/{project} | awk '{{if (match($3,"/")){{ print $3}}}}' )
cp -L -n $deplist ./{dist_folder}"""
    os.system(copy_command)

    if copy_data_list is not None:
        for data in copy_data_list:
            if os.path.exists(data):
                os.system(f'cp {data} -R ./{dist_folder}/')  # works with folder OR file
    if dependent_packages is not None:
        package_list = f"({' '.join(dependent_packages)})"
    else:
        package_list = ''
    project_deb = f'{project}_deb'
    user_name = os.getlogin()
    DEBIAN_path = f'./{project_deb}/DEBIAN'
    application_path = f'./{project_deb}/usr/share/applications'
    icons_path = f'./{project_deb}/usr/share/icons'
    lib_project_path = f'./{project_deb}/usr/lib/{project}'
    res_dir = f'{lib_project_path}/res'

    # 图标文件
    project_icon = ''
    if os.path.exists(f'{project}.ico'):
        project_icon = f'{project}.ico'
    elif os.path.exists(f'{project}.svg'):
        project_icon = f'{project}.svg'
    elif os.path.exists(f'{project}.png'):
        project_icon = f'{project}.png'
    elif os.path.exists(f'{project}.bmp'):
        project_icon = f'{project}.bmp'
    # control terminal showing
    terminal = 'true' if show_terminal else 'false'

    os.makedirs(DEBIAN_path, exist_ok=True)
    os.makedirs(icons_path, exist_ok=True)
    os.makedirs(application_path, exist_ok=True)
    os.makedirs(lib_project_path, exist_ok=True)

    control = f'''Package: {project}
Version: {version}
Architecture: {architecture}
Maintainer: {maintainer}
Description: {description}
'''
    # 写上sudo在运行进需要管理员权限，但是仍算是用户目录下，而不是根目录
    postinst = f"""#! /bin/bash
echo "initialize the environment necessary"
echo {root_password} | sudo cp /usr/share/applications/{project}.desktop ~/Desktop
echo {root_password} | sudo mkdir -p res
packages={package_list}
for app in ${{packages[@]}};do
    echo {root_password} | sudo apt install ${{app}}
    sleep 5
done
echo "all needed files are installed correctly"

sleep 5

echo POST INSTALLATION FUNCTION EXECUTED
"""

    desktop = f"""[Desktop Entry]
Categories=Office
Comment={description}
Exec=/usr/lib/{project}/{project}
Icon=/usr/share/icons/{project_icon}
Name={project}
Terminal={terminal}
Type=Application
X-Deepin-Vendor=user-custom
X-Ubuntu-Touch=true
"""

    with open(f'{DEBIAN_path}/control', 'w', encoding='utf8') as f:
        f.write(control)

    with open(f'{DEBIAN_path}/postinst', 'w', encoding='utf8') as f:
        f.write(postinst)

    with open(f'{application_path}/{project}.desktop', 'w', encoding='utf8') as f:
        f.write(desktop)

    if os.path.exists('res'):
        os.system(f'cp -R ./res {lib_project_path}')
        os.system(f'cp res/{project_icon} {icons_path}')
    elif os.path.exists(f'{project_icon}'):
        os.system(f'cp {project_icon} {icons_path}')

    src_dir = f'./{dist_folder}'
    dst_dir = f'./{project_deb}/usr/lib/{project}'
    os.system(f'chmod 775 {DEBIAN_path}/postinst')
    os.system(f'cp -R {src_dir}/* {dst_dir}')
    time.sleep(5)
    os.system(f'dpkg -b {project_deb} {project}_{version}_arm64.deb')
    if cleanup:
        os.system(f'rm -R {project_deb}')
        os.system(f'rm {project_deb}.spec')
    os.system(f'echo {root_password} | sudo -S dpkg -i {project}_{version}_arm64.deb')


def findChineseDigits(original_string):
    import re
    strings = re.findall('[一二三四五六七八九十零百千]+', original_string)
    return strings


def chinese2ArabicDigits(string, fill_width=2):
    if string == '十':  # or string.endswith('一十')
        sub_string = '10'
    else:
        trans_dict = ''.maketrans(
            {'零': '0', '一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8',
             '九': '9'})
        sub_string = string.translate(trans_dict)
        if sub_string.startswith('十'):
            sub_string = sub_string.replace('十', '1')
        for i in '十百千万亿':
            if string.endswith(i):
                sub_string = sub_string.replace(i, '0')
            else:
                sub_string = sub_string.replace(i, '')
    fill_zeros = fill_width - len(sub_string)
    if fill_zeros > 0:
        sub_string = fill_zeros * '0' + sub_string

    return sub_string


def chinese2Arabic(original_string):
    strings = findChineseDigits(original_string)
    new_strings = original_string
    for string in strings:
        new_strings = new_strings.replace(string, chinese2ArabicDigits(string))
    return new_strings


def pathName2ArabicDigits(path):
    os.renames(path, chinese2Arabic(path))


def getFullSubfoldersAndFiles(path, level=-1):
    root_path, subfolders, files = list(os.walk(path))[0]
    full_subfolders = [os.path.join(root_path, subfolder) for subfolder in subfolders]
    full_files = [os.path.join(root_path, file) for file in files]
    if level == -1:
        pass
    else:
        pass
    return full_subfolders, full_files


def dirContents2ArabicDigits(path):
    folders, files = getFullSubfoldersAndFiles(path)
    for path in folders + files:
        pathName2ArabicDigits(path)


def listenClipboard():
    """后台脚本：每隔0.2秒，读取剪切板文本，检查有无指定字符或字符串，如果有则执行替换"""
    # recent_txt 存放最近一次剪切板文本，初始化值只多执行一次paste函数读取和替换
    recent_txt = pyperclip.paste()
    while True:
        # txt 存放当前剪切板文本
        txt = pyperclip.paste()
        # 剪切板内容和上一次对比如有变动，再进行内容判断，判断后如果发现有指定字符在其中的话，再执行替换
        if txt != recent_txt:
            # print(f'txt:{txt}')
            recent_txt = txt  # 没查到要替换的子串，返回None
            return recent_txt

        # 检测间隔（延迟0.2秒）
        time.sleep(0.2)


def shutDownComputer():
    os.system('shutdown /s /t 0 /f')


if __name__ == '__main__':
    # dirContents2ArabicDigits(r'E:\python\天翼云盘下载\家庭养生')
    setScheduled(print, args='cddd', trigger='cron', hour='17')
    ...
