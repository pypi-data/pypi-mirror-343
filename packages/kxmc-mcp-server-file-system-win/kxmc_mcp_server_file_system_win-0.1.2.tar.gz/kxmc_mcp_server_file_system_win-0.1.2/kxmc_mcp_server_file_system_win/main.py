#!/usr/bin/python3
import os
import shutil

from mcp.server import FastMCP

# """
# 日志配置
# """
# # 获取当前时间
# now = datetime.now()
# # 格式化为 '年_月_日_时_分_秒' 的形式
# # formatted_time = now.strftime("%Y_%m_%d_%H_%M_%S")
# formatted_time = now.strftime("%Y_%m_%d_%H")
# log_instance = LogUtil(f"log_name_server_fir_dir_operation_{formatted_time}",
#                        f"log_file_server_fir_dir_operation_{formatted_time}").logger
"""
初始化MCP服务
"""
mcp = FastMCP("fir_dir_Operation_mcp")


@mcp.tool()
def create_file(file_path) -> str:
    """
    根据提供的路径创建文件
    :param file_path: 文件的完整路径
    """
    result = "创建文件失败"
    try:
        # 打开文件以写入模式，如果文件不存在则创建
        with open(file_path, 'w') as file:
            result = f"文件 {file_path} 创建成功"
    except FileExistsError:
        result = f"文件 {file_path} 已存在"
        # log_instance.error(result)
    except Exception as e:
        result = f"创建文件时出错: {e}"
        # log_instance.error(result)
    return result


@mcp.tool()
def create_directory(dir_path) -> str:
    """
    根据提供的路径创建目录
    :param dir_path: 目录的完整路径
    """
    try:
        # 创建目录，如果目录已存在会抛出 FileExistsError
        os.makedirs(dir_path)
        result = f"目录 {dir_path} 创建成功"
        # log_instance.info(result)
    except FileExistsError:
        result = f"目录 {dir_path} 已存在"
        # log_instance.error(result)
    except Exception as e:
        result = f"创建目录时出错: {e}"
        # log_instance.error(result)
    return result


@mcp.tool()
def copy_file(source_file, destination_file) -> str:
    """
    复制文件
    :param source_file: 源文件的完整路径
    :param destination_file: 目标文件的完整路径
    """
    try:
        # 复制文件
        shutil.copy2(source_file, destination_file)
        result = f"文件从 {source_file} 复制到 {destination_file} 成功"
        # log_instance.info(result)
    except FileNotFoundError:
        result = f"源文件 {source_file} 未找到"
        # log_instance.error(result)
    except Exception as e:
        result = f"复制文件时出错: {e}"
        # log_instance.error(result)
    return result


"""
MCP服务配置：

run
--directory
D:\\code\\PythonProject\\MCPTest\\mcp-client
mcp_server_file_dir_operations.py

"""

def main():
    # # 示例：创建文件
    # file_path = "filedirtest\\test_file.txt"
    # create_file(file_path)
    #
    # # 示例：创建目录
    # dir_path = "filedirtest\\test_directory"
    # create_directory(dir_path)
    #
    # # 示例：复制文件
    # source = "filedirtest\\test_file.txt"
    # destination = "filedirtest\\test_directory\\test_file_copy.txt"
    # copy_file(source, destination)

    # print("mcp服务已开启")
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
