import os
from mcp.server.fastmcp import FastMCP
from mcp_deploy.mcp_handlers import createworkspace, uploadfile, execute
from mcp_deploy.mcp_handlers import File

mcp = FastMCP("mcp-deploy")

api_token = os.environ.get("API_TOKEN")
if not api_token:
    raise ValueError("API_TOKEN environment variable is required")
region = os.environ.get("region", "ap-shanghai")

@mcp.tool()
def create_workspace() -> dict:
    """创建新的Cloud Studio工作空间 [MCP标准]
    
    功能说明:
    - 创建一个全新的Cloud Studio工作空间实例
    - 使用环境变量中的API_TOKEN进行认证
    - 返回包含工作空间ID的字典
    
    参数要求:
    - 无直接输入参数
    - 依赖环境变量:
      * API_TOKEN: 有效的认证令牌(必填)
    
    返回值:
    {
        "workspace_id": "str",  # 工作空间唯一ID(格式:ws-xxxxxx)
    }
    
    注意事项:
    1. 需要预先设置API_TOKEN环境变量
    2. 每个API_TOKEN有创建频率限制
    3. 返回的workspace_key需要妥善保存
    
    典型响应:
    {
        "workspace_key": "ws-kmhhvqnlogr0il1pyvc48",
        "webIDE": "https://ws-kmhhvqnlogr0il1pyvc48--ide.ap-shanghai.cloudstudio.club",
    }
    """
    result = createworkspace(api_token)
    return result

@mcp.tool()
def write_files(workspace_key: str, region: str, files: list[File]) -> str:
    """上传文件到指定工作空间
    
    将多个文件上传到Cloud Studio工作空间，支持文本文件内容的上传。
    
    Args:
        workspace_id (str): 目标工作空间ID，格式如'ws-xxxxxx'
        files (list[File]: 要上传的文件列表，每个File对象包含:
            - save_path: str 文件在workspace中的相对路径
            - file_content: str 文件内容(UTF-8编码)
            
    Returns:
        str: 上传结果信息("上传文件成功"或"上传文件失败")
        工具默认上传到/workspace目录下
        
    Raises:
        ValueError: 如果workspace_id格式无效
        IOError: 如果文件上传过程中出现错误
        TypeError: 如果files参数格式不正确
        
    Example:
        >>> write_files("ws-123", "files":[{"save_path"="/example/test.txt", "file_content"="print(hello world"))])
        '上传文件成功'
    """

    if workspace_key is None or not workspace_key.startswith("ws-"):
        raise ValueError("Invalid workspace_id format")
    if not files:
        raise ValueError("No files to upload")
    
    success = uploadfile(api_token, workspace_key, region, files)
    return success

@mcp.tool()
def execute_command(workspace_key: str, region: str, command: str) -> str:
    """在工作空间中执行命令
    
    在指定的Cloud Studio工作空间中执行shell命令并返回结果。
    
    Args:
        workspace_key (str): 目标工作空间ID，格式如'ws-xxxxxx'
        region (str): 工作空间所在区域，如'ap-shanghai'
        command (str): 要执行的shell命令
        
    Returns:
        str: 命令执行结果输出
        
    Raises:
        RuntimeError: 如果命令执行失败
        ConnectionError: 如果无法连接到工作空间
        
    Example:
        >>> execute_command("ws-xxxx", "ap-shanghai", "ls -al")
        'total 4\n-rw-r--r-- 1 root root 12 Jan 1 00:00 test.txt'
    """

    if workspace_key is None or not workspace_key.startswith("ws-"):
        raise ValueError("Invalid workspace_id format")
    if not command:
        raise ValueError("Command cannot be empty")
    
    result = execute(api_token, workspace_key, region, command)
    return result

def main():
    mcp.run()

if __name__ == "__main__":
    main()