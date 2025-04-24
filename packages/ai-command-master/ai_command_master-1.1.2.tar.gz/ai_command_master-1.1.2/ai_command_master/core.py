"""核心逻辑模块
该模块负责处理整个应用程序的核心流程，包括：
- 用户输入处理
- 配置文件管理
- API调用
- 命令执行
- 系统信息收集
"""

from .execution import Execution
from .system import SystemInfo
from .config import ConfigManager
from .data_formatter import DataFormatter
from .api_clients.factory import APIClientFactory


# 全局配置管理器实例（单例模式）
config_instance: ConfigManager = ConfigManager()

# 显示当前配置
def show_config():
    active_profile = config_instance.get_active_profile()
    print(f'AICli> 当前用户配置文件是 "{active_profile}" ，输入 "ai config switch <配置文件名>" 切换用户配置文件。')

# 列出所有配置文件
def list_all_profiles():
    try:
        config_profiles: list = config_instance.get_available_profiles()
        if config_profiles:
            print(f"AICli> 所有用户配置文件: ")
            for profile in config_profiles:
                print(f" - {profile}")
            print(f'输入 "ai config switch <配置文件名>" 可切换配置文件。')
        else:
            print(f'AICli> 没有找到用户配置文件，输入 "ai config create <配置文件名>" 创建用户配置文件。')
    except Exception as e:
        print(f"Error: {e}")

# 切换配置文件
def switch_config(profile_name: str):
    is_success = config_instance.switch_profile(profile_name)
    if not is_success:
        print(f'AICli> 切换用户配置文件失败，请检查用户配置文件 {profile_name} 是否存在。')

# 新建配置文件
def create_profile(profile_name: str):
    # 初始化配置文件模板
    config_content: dict = {
        "model_provider":"",
        "model":"",
        "base_url":"",
        "api_key":"",
        "max_token":2000,
        "temperature":0.3,
    }

    print(f'AICli> 用户配置文件命名建议直接使用模型名，用全小写字母，不同单词用下划线分隔，如 "deepseek_chat" 。')

    try:
        for key, value in config_content.items():
            if key == "max_token":
            # 将输入转换为整数
                config_content[key] = int(input(f" - 请输入{key}的值（取值区间[1,8192]，默认2000）: "))
            elif key == "temperature":
            # 将输入转换为浮点数
                config_content[key] = float(input(f" - 请输入{key}的值（取值区间[0,1]，默认0.3）: "))
            else:
                config_content[key] = input(f" - 请输入{key}的值: ")
    except ValueError as e:
        pass
        # print('AICli> "max_token" 和 "temperature" 的值为数字。')

    is_success = config_instance.create_profile(profile_name, config_content)
    if not is_success:
        print(f'AICli> 创建用户配置文件失败，请检查用户配置文件 {profile_name} 是否已存在。')
    else:
        print(f'AICli> 已自动切换到配置文件 "{profile_name}" ，可以通过 "ai config show" 查看当前配置文件。')


def update_profile(profile_name: str):
    is_success = config_instance.update_profile(profile_name)
    if not is_success:
        print(f'AICli> 更新用户配置文件失败，请检查用户配置文件 "{profile_name}" 是否存在。')
    else:
        print(f'AICli> 已更新并切换到用户配置文件 "{profile_name}" ，可以通过 "ai config show" 查看当前配置文件。')


def delete_profile(profile_name: str):
    """删除配置文件

    Returns:
        bool: 删除结果
    """
    is_success = config_instance.delete_profile(profile_name)
    if not is_success:
        print(f'AICli> 删除用户配置文件失败，请检查用户配置文件 "{profile_name}" 是否存在。')
    else:
        print(f'AICli> 已删除用户配置文件 "{profile_name}" ，可以通过 "ai config list" 查看所有配置文件。')


def load_config() -> dict:
    """加载应用程序配置
    
    Returns:
        dict: 包含所有配置项的字典
    """
    config = config_instance.load_config()
    return config


def load_system_info() -> dict:
    """收集当前系统环境信息
    
    Returns:
        dict: 包含系统信息的字典，包括操作系统类型、版本、用户信息等
    """
    system_info = SystemInfo()
    return system_info.get_system_info()


def prepare_message(user_message: str, config_args: dict, system_args: dict) -> list:
    """准备发送给AI模型的消息
    
    Args:
        user_message (str): 用户输入的原始消息
        config_args (dict): 应用程序配置参数
        system_args (dict): 系统环境信息
    
    Returns:
        list: 格式化后的消息列表，包含system和user角色的消息
    """
    messages: list = []
    
    prompt: str = config_args['prompt']['base']
    
    system_info = {
        "prompt": prompt,
        "system_info": {
            "os": system_args['系统'],
            "os_version": system_args['系统版本'],
            "username": system_args['用户名'],
            "home_dir": system_args['用户家目录'],
            "current_dir": system_args['当前工作目录']
        }
    }

    messages.append({
        "role": "system",
        "content": str(system_info)
    })
    messages.append({
        "role": "user",
        "content": user_message
    })

    return messages


def call_api(config_args: dict, messages: list) -> str:
    """调用AI模型API
    
    Args:
        config_args (dict): 包含API配置的字典
        messages (list): 待发送的消息列表
    
    Returns:
        str: AI模型的原始响应文本
    """
    provider = config_args['model_provider']
    client = APIClientFactory.get_api_client(provider, config_args)
    response = client.chat_completion(messages)
    client.close()
    return response


def format_response(response: str) -> dict:
    """解析和格式化AI模型的响应
    
    Args:
        response (str): AI模型的原始响应文本
    
    Returns:
        dict: 解析后的结构化响应数据
    """
    response_formatter = DataFormatter(response)
    response_dict = response_formatter.parse()
    return response_dict


def saft_execution(model: str, response_dict: dict):
    """安全地执行AI模型生成的命令
    
    Args:
        model (str): 使用的AI模型标识符
        response_dict (dict): 解析后的AI响应数据
    """
    exe = Execution(model, response_dict)
    exe.execute()


def start_request(full_description: str):
    """处理用户请求的主流程
    
    整个处理流程包括：
    1. 接收用户输入
    2. 加载配置
    3. 收集系统信息
    4. 准备AI消息
    5. 调用AI接口
    6. 解析响应
    7. 执行命令
    
    Args:
        full_description (str): 用户的完整输入描述
    """
    # 1. 获取用户输入
    user_message: str = full_description
    # print(f"User message: {user_message}\n")
    
    # 2. 加载配置
    config_args: dict = load_config()
    # print(f"Config args: {config_args}\n")
    
    # 3. 收集系统信息
    system_args: dict = load_system_info()
    # print(f"System args: {system_args}\n")
    
    # 4. 准备消息
    messages: list = prepare_message(user_message, config_args, system_args)
    # print(f"Prepared messages: {messages}\n")
    
    # 5. 调用API获取结果
    response: str = call_api(config_args, messages)
    # print(f"API response: {response}\n")

    # 6. 格式化返回结果
    response_dict: dict = format_response(response)
    # print(f"Formatted response: {response_dict}\n")

    # 7. 安全执行
    saft_execution(config_args['model'], response_dict)


if __name__ == '__main__':
    start_request("怎么查看网络配置")