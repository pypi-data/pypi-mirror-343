#!/usr/bin/python
import os

import click
import hashlib

from git import Repo
from pathlib import Path

# 工具初始化

# git 仓库中更新的文件
updated = []

# git 仓库相关对象
repo_ok = False
repo = None
index = None
remote = None

try:
    # 初始化仓库
    repo = Repo(Path(__file__).parent.__str__())

    # 用来 add commit 等
    index = repo.index
    # 进行远程操作
    remote = repo.remote()

    # 仓库初始化成功
    repo_ok = True

except Exception as e:
    click.echo("远程仓库未设置! 请先设置仓库!")
    # sys.exit()


# 文件夹备份到
BACKUP_FOLDER = Path(__file__).parent.__str__() + "/configs/"

# 默认要备份的文件夹列表
FILE_LIST = Path(__file__).parent.__str__() + "/files.txt"

# Home path
HOME_PATH = Path.home().__str__()

# 配置文件列表文件
config_files: list[str] = []


def getBackUpPath(source_path: str):
    """
    获取备份文件的备份地址!
    """

    # 将 source 路径改为 ~/?? 路径
    if not source_path.startswith("~"):
        temp = os.path.abspath(source_path)
        source_path = temp.replace(HOME_PATH, "~")
    else:
        source_path = os.path.abspath(source_path)

    return (
        BACKUP_FOLDER
        + hashlib.md5(str(source_path).encode("utf8")).hexdigest()
        + "-"
        + Path(source_path).name
    )


def getResourceFilePath(file_path: str):
    """
    获取配置文件源地址! 返回绝对路径!
    ~/xx/xx.cfg -> /fol/xx.cfg
    ../xx/xxcfg -> /fol/xx.cfg
    """
    if file_path.startswith("~"):
        return str(Path(file_path).expanduser())
    else:
        return str(Path(file_path).absolute())


def copyFile(from_f: str, to_f: str):
    """
    复制文件, 权限不足时 , 使用 sudo
    1. 判断父文件夹是否存在,不存在就创建文件夹
    """
    parent_dir = Path(to_f).parent
    if (not parent_dir.exists()):
        os.system(f'sudo mkdir -p -m 777 {str(parent_dir)}')

    if os.access(to_f, os.W_OK):
        os.system(f"cp -af {str(from_f)} {str(to_f)}")
    else:
        os.system(f"sudo cp -af {str(from_f)} {str(to_f)}")


def loadConfigFileList():
    """
    加载备份文件列表, 从相对路径到绝对路径
    ~  --->  /
    """
    # 清空列表
    config_files.clear()

    if not Path(BACKUP_FOLDER).exists():
        # 创建备份文件夹
        os.makedirs(BACKUP_FOLDER)

    if Path(FILE_LIST).exists():
        # 判断文件是否存在
        with open(FILE_LIST) as f:
            for line in f:
                # 加载列表
                config_files.append(
                    getResourceFilePath(line).replace("\n", ""))
    else:
        # 创建备份列表文件
        open(FILE_LIST, "w").close()

        if repo_ok:
            # 添加新建的备份列表到仓库中
            updated.append(FILE_LIST)
            index.add(updated)

            index.commit("创建配置文件记录列表!")


@click.group()
def main():
    """
    linux 配置文件备份命令行工具!
    """
    loadConfigFileList()


@main.command("l")
def listRecorded():
    """
    列出所有已经备份的文件!
    """
    with open(FILE_LIST) as f:
        for index, line in enumerate(f):
            click.echo(f"{index} {line.strip()}")


@main.command("b")
@click.argument("files", nargs=-1)
def backup(files):
    """
    同步配置文件到备份文件夹!
    """
    if len(files) == 0:
        # 将待备份文件设置为所有文件
        files = config_files

    for file in files:
        # 获取源文件路径 和 备份文件路径
        source_path = getResourceFilePath(file)
        backup_path = getBackUpPath(file)

        if Path(source_path).exists() and Path(backup_path).exists():
            # 需要备份的文件存在
            source_file_st_time = Path(source_path).stat().st_mtime
            backup_file_st_time = Path(backup_path).stat().st_mtime

            if source_file_st_time > backup_file_st_time:
                # 判断需要备份的文件与已经备份的文件新旧
                updated.append(backup_path)
                click.echo(f"更新备份文件 -> {source_path}")

                copyFile(source_path, backup_path)

                if repo_ok:
                    index.add([backup_path, FILE_LIST])
                    index.commit(f"更新配置文件 -> {source_path}")
            else:
                click.echo(f"文件不需要更新 -> {source_path}")
        else:
            if not Path(source_path).exists():
                click.echo(f"待备份文件不存在 -> {source_path}")
                continue  # 继续处理下一个

            if not Path(backup_path).exists():
                # click.echo(f"已备份文件不存在 -> {backup_path}")

                copyFile(source_path, backup_path)

                if source_path not in config_files:
                    # 添加新的记录
                    with open(FILE_LIST, "a") as f:
                        click.echo(f"已备份文件不存在 -> {backup_path}")

                        record = source_path.replace(HOME_PATH, "~")
                        click.echo(f"新增文件备份记录 -> {record}")
                        f.write(record + "\n")

                    if repo_ok:
                        index.add([backup_path, FILE_LIST])
                        index.commit(f"添加配置文件 -> {source_path}")
                continue  # 继续处理下一个


@main.command("u")
@click.argument("files", nargs=-1)
def update(files):
    """
    从备份文件夹中恢复指定文件!
    """
    if len(files) == 0:
        # 将待更新文件设置为所有文件
        files = config_files

    for file in files:
        # 更新本地配置文件
        click.echo(f"更新本地文件 -> {file}")

        from_f = getBackUpPath(file)
        to_f = getResourceFilePath(file)

        copyFile(from_f, to_f)


@main.command("P")
def push():
    """
    将本地备份推送到远程仓库!
    """
    if not repo_ok:
        click.echo("远程仓库未设置! 请先设置仓库!")
        return
    try:
        remote.push()
    except Exception as e:
        click.echo(e)


@main.command("p")
def pull():
    """
    从云端拉取最新的配置文件!
    """
    if not repo_ok:
        click.echo("远程仓库未设置! 请先设置仓库!")
        return
    try:
        remote.pull()
    except Exception as e:
        click.echo(e)


@main.command("d")
@click.argument("idx", nargs=1, type=click.INT)
@click.pass_context
def deleteConfigFile(ctx: click.Context, idx):
    """
    删除给定配置文件!
    """
    try:
        deleted_file = config_files.pop(idx)
    except:
        ctx.invoke(listRecorded)
        click.echo("请输入正确序号!")
        return

    # 删除备份文件
    backup_file_path = getBackUpPath(deleted_file)
    os.system(f"rm {backup_file_path}")

    # 写入列表
    with open(FILE_LIST, "w") as f:
        for file in config_files:
            f.write(file.replace(HOME_PATH, "~") + "\r")

    message = f"删除配置文件 -> {deleted_file}"
    click.echo(message)

    if not repo_ok:
        click.echo("远程仓库未设置! 请先设置仓库!")
        return
    else:
        index.commit(message)


if __name__ == "__main__":
    main()
