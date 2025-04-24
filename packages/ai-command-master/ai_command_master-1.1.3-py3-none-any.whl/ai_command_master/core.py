"""核心逻辑模块 (Core Logic Module)

该模块负责处理整个应用程序的核心流程，包括：
- 用户输入处理 (User input processing)
- 配置文件管理 (Configuration file management)
- API调用 (API calls)
- 命令执行 (Command execution)
- 系统信息收集 (System information gathering)
"""

import json
from typing import Dict, Any, List, Optional

# 假设这些模块在同一目录下或已正确安装
from .execution import Execution
from .system import SystemInfo
from .config import ConfigManager
from .data_formatter import DataFormatter
from .api_clients.factory import APIClientFactory


# 全局配置管理器实例（单例模式）
# Global ConfigManager instance (Singleton)
config_instance: ConfigManager = ConfigManager()

# --- Configuration Management Functions ---

def show_config() -> None:
    """显示当前活动的配置文件名称。
    Displays the name of the currently active configuration profile.
    """
    active_profile: str = config_instance.get_active_profile()
    print(f'AICli> 当前用户配置文件是 "{active_profile}"。')
    # if active_profile == 'default':
    #     print(f'AICli> 注意: 默认配置文件 "default" 是只读的模板文件，请及时切换到其他配置文件。')
    print(f'AICli> 输入 "ai config switch <配置文件名>" 可切换用户配置文件。')
    # 可选：显示部分关键配置
    # Optional: Display some key configuration values
    # current_config = config_instance.get_config()
    # print(f"  - 模型提供商 (Model Provider): {current_config.get('model_provider', '未设置')}")
    # print(f"  - 模型 (Model): {current_config.get('model', '未设置')}")

def list_all_profiles() -> None:
    """列出所有可用的用户配置文件。
    Lists all available user configuration profiles.
    """
    try:
        config_profiles: List[str] = config_instance.get_available_profiles()
        print("AICli> 可用的用户配置文件:")
        print("  - default (系统默认)") # Explicitly mention default
        if config_profiles:
            for profile in config_profiles:
                print(f"  - {profile}")
            print(f'\nAICli> 输入 "ai config switch <配置文件名>" 可切换配置文件。')
            print(f'AICli> 输入 "ai config update <配置文件名>" 可更新配置文件。')
            print(f'AICli> 输入 "ai config delete <配置文件名>" 可删除配置文件。')
        else:
            print(f'AICli> (没有找到其他用户配置文件)')
            print(f'\nAICli> 输入 "ai config create <配置文件名>" 可创建新的用户配置文件。')
    except Exception as e:
        print(f"AICli> 错误: 列出配置文件时出错: {e}")

def switch_config(profile_name: str) -> None:
    """切换到指定的配置文件。
    Switches to the specified configuration profile.

    Args:
        profile_name (str): 要切换到的配置文件名称。
                           The name of the profile to switch to.
    """
    if not profile_name:
        print("AICli> 错误: 需要提供配置文件名称。")
        list_all_profiles() # Show available profiles for help
        return

    is_success: bool = config_instance.switch_profile(profile_name)
    # switch_profile 内部已经打印了成功或失败的消息
    # The switch_profile method already prints success/failure messages
    # if not is_success:
    #     print(f'AICli> 切换用户配置文件失败，请检查用户配置文件 "{profile_name}" 是否存在。')

def create_profile(profile_name: str) -> None:
    """交互式地创建新的用户配置文件。
    Interactively creates a new user configuration profile.

    Args:
        profile_name (str): 新配置文件的名称。
                           The name for the new profile.
    """
    if not profile_name or not profile_name.strip():
        print("AICli> 错误: 配置文件名称不能为空。")
        return
    if profile_name.lower() == 'default':
        print("AICli> 错误: 不能创建名为 'default' 的配置文件，它是保留名称。")
        return

    print(f"AICli> 正在创建新的配置文件: '{profile_name}'")
    print(f'AICli> 提示: 配置文件名建议使用全小写字母和下划线，例如 "deepseek_chat"。')
    print("AICli> 请输入以下配置项的值 (直接按 Enter 可跳过并使用默认值或留空):")

    # 使用 ConfigManager 中定义的更新逻辑或类似的交互方式可能更一致
    # Consider using update logic similar to ConfigManager for consistency
    # 这里我们简化处理，但添加了基本的验证
    config_content: Dict[str, Any] = {
        "model_provider": None,
        "model": None,
        "base_url": None,
        "api_key": None,
        "max_token": 2000, # Default value
        "temperature": 0.3, # Default value
    }
    input_data: Dict[str, Any] = {}

    try:
        # --- 获取用户输入 ---
        provider = input("  - model_provider (例如: openai, google, ollama): ").strip()
        if provider: input_data["model_provider"] = provider

        model = input("  - model (例如: gpt-4, gemini-pro, llama3): ").strip()
        if model: input_data["model"] = model

        base_url = input("  - base_url (API 基地址, 留空则使用默认): ").strip()
        if base_url: input_data["base_url"] = base_url

        api_key = input("  - api_key (API 密钥): ").strip()
        if api_key: input_data["api_key"] = api_key

        max_token_str = input(f"  - max_token (整数, 1-8192, 默认 {config_content['max_token']}): ").strip()
        if max_token_str:
            try:
                max_token = int(max_token_str)
                if 1 <= max_token <= 8192:
                    input_data["max_token"] = max_token
                else:
                    print(f"    警告: max_token 值 '{max_token}' 超出范围 [1, 8192]，将使用默认值 {config_content['max_token']}。")
            except ValueError:
                print(f"    警告: 输入的 max_token '{max_token_str}' 不是有效整数，将使用默认值 {config_content['max_token']}。")

        temperature_str = input(f"  - temperature (浮点数, 0.0-1.0, 默认 {config_content['temperature']}): ").strip()
        if temperature_str:
            try:
                temperature = float(temperature_str)
                if 0.0 <= temperature <= 1.0:
                    input_data["temperature"] = temperature
                else:
                     print(f"    警告: temperature 值 '{temperature}' 超出建议范围 [0.0, 1.0]，将使用默认值 {config_content['temperature']}。")
            except ValueError:
                print(f"    警告: 输入的 temperature '{temperature_str}' 不是有效浮点数，将使用默认值 {config_content['temperature']}。")

        # 合并用户输入和默认值
        final_config = config_content.copy() # Start with defaults
        final_config.update(input_data) # Overwrite with user input where provided

        # 清理掉值为 None 的键 (用户未输入的)
        final_config = {k: v for k, v in final_config.items() if v is not None}

        # --- 创建配置文件 ---
        is_success: bool = config_instance.create_profile(profile_name, final_config)
        # create_profile 内部会打印成功或失败信息并自动切换
        # The create_profile method prints messages and switches automatically
        # if is_success:
        #     print(f'AICli> 已创建并自动切换到配置文件 "{profile_name}"。')
        # else:
        #     print(f'AICli> 创建用户配置文件失败。请检查名称是否已存在或是否有写入权限。')

    except (EOFError, KeyboardInterrupt):
        print("\nAICli> 操作已取消。")
    except Exception as e:
        print(f"AICli> 创建配置文件时发生意外错误: {e}")

def update_profile(profile_name: Optional[str] = None) -> None:
    """交互式地更新指定的配置文件。如果未提供名称，则更新当前活动的配置。
    Interactively updates the specified configuration profile.
    If no name is provided, updates the currently active profile.

    Args:
        profile_name (Optional[str]): 要更新的配置文件名称。如果为 None，则更新当前活动配置。
                                      The name of the profile to update. If None, updates the active profile.
    """
    target_profile = profile_name if profile_name else config_instance.get_active_profile()

    if not target_profile:
         print("AICli> 错误: 无法确定要更新哪个配置文件。")
         return

    if target_profile.lower() == 'default':
        print("AICli> 提示: 'default' 配置文件是只读模板，不能直接更新。")
        print("AICli> 如需修改默认设置，请编辑 'config/default.yaml' 文件。")
        print("AICli> 如需创建自定义配置，请使用 'ai config create <名称>' 命令。")
        return

    print(f"AICli> 准备更新配置文件: '{target_profile}'")
    is_success: bool = config_instance.update_profile(target_profile)
    # update_profile 内部会打印详细的更新过程和结果
    # The update_profile method prints detailed update process and results
    # if is_success:
    #      print(f'AICli> 配置文件 "{target_profile}" 更新完成。')
    # else:
    #      print(f'AICli> 更新用户配置文件 "{target_profile}" 失败。请检查文件是否存在或格式是否正确。')


def delete_profile(profile_name: str) -> None:
    """删除指定的用户配置文件。
    Deletes the specified user configuration profile.

    Args:
        profile_name (str): 要删除的配置文件名称。
                           The name of the profile to delete.
    """
    if not profile_name or not profile_name.strip():
        print("AICli> 错误: 需要提供要删除的配置文件名称。")
        list_all_profiles()
        return
    if profile_name.lower() == 'default':
        print("AICli> 错误: 不能删除 'default' 配置文件。")
        return

    # 添加确认步骤
    try:
        confirm = input(f"AICli> 警告: 您确定要删除配置文件 '{profile_name}' 吗? 这个操作无法撤销。[Y/N]: ").strip().lower()
        if confirm != 'y':
            print("AICli> 操作已取消。")
            return
    except (EOFError, KeyboardInterrupt):
        print("\nAICli> 操作已取消。")
        return

    is_success: bool = config_instance.delete_profile(profile_name)
    # delete_profile 内部会打印成功或失败消息
    # The delete_profile method prints success/failure messages
    # if is_success:
    #     print(f'AICli> 已删除用户配置文件 "{profile_name}"。')
    #     # list_all_profiles() # Optionally show remaining profiles
    # else:
    #     print(f'AICli> 删除用户配置文件 "{profile_name}" 失败。请检查文件是否存在。')

# --- Core Workflow Functions ---

def load_config() -> Dict[str, Any]:
    """加载当前活动的应用程序配置。
    Loads the currently active application configuration.

    Returns:
        Dict[str, Any]: 包含所有配置项的字典。
                       A dictionary containing all configuration items.
    """
    # load_config 内部会处理加载逻辑和错误
    # The load_config method handles loading logic and errors internally
    return config_instance.load_config()

def load_system_info() -> Dict[str, Any]:
    """收集当前系统环境信息。
    Gathers information about the current system environment.

    Returns:
        Dict[str, Any]: 包含系统信息的字典。
                       A dictionary containing system information.
    """
    try:
        system_info = SystemInfo()
        return system_info.get_system_info()
    except Exception as e:
        print(f"AICli> 警告: 收集系统信息时出错: {e}")
        return {} # Return empty dict on error

def prepare_message(user_message: str, config_args: Dict[str, Any], system_args: Dict[str, Any]) -> List[Dict[str, str]]:
    """准备发送给 AI 模型的消息列表。
    Prepares the list of messages to send to the AI model.

    Args:
        user_message (str): 用户输入的原始消息 (User's original message).
        config_args (Dict[str, Any]): 应用程序配置参数 (Application configuration parameters).
        system_args (Dict[str, Any]): 系统环境信息 (System environment information).

    Returns:
        List[Dict[str, str]]: 格式化后的消息列表 (Formatted list of messages).
    """
    messages: List[Dict[str, str]] = []

    # 安全地获取基础提示，并提供一个通用的默认值
    # Safely get the base prompt, providing a generic default
    base_prompt: str = config_args.get('prompt', {}).get('base', "You are a helpful AI assistant operating in a command line environment.")

    # 构建系统信息部分，使其更易于LLM解析 (例如使用JSON格式)
    # Structure system info for better LLM parsing (e.g., using JSON)
    system_context = {
        "role_instruction": base_prompt,
        "environment": {
            "os": system_args.get('系统', 'Unknown'),
            "os_version": system_args.get('系统版本', 'Unknown'),
            "username": system_args.get('用户名', 'Unknown'),
            "home_dir": system_args.get('用户家目录', 'Unknown'),
            "current_dir": system_args.get('当前工作目录', 'Unknown'),
            # 可以添加更多相关信息，如 Shell 类型等
            # More info can be added, like Shell type etc.
        },
         "output_format_hint": """\
Please provide your response in the following JSON format inside a single code block:
```json
{
  "explanation": "Brief explanation of the command(s).",
  "commands": [
    {"command": "command_to_execute_1", "description": "What this command does."},
    {"command": "command_to_execute_2", "description": "What this command does."}
  ],
  "alternative_commands": [
     {"command": "alternative_command_1", "description": "When to use this alternative."},
     {"command": "alternative_command_2", "description": "Another alternative."}
  ],
  "warnings": [
    "Potential risks or important notes."
  ],
  "confidence_score": 0.9 // A score between 0.0 and 1.0 indicating confidence
}
```"""
    }

    # 将系统上下文转换为字符串（例如 JSON 字符串）
    # Convert system context to string (e.g., JSON string)
    system_content = json.dumps(system_context, indent=2, ensure_ascii=False)

    messages.append({"role": "system", "content": system_content})
    messages.append({"role": "user", "content": user_message})

    return messages

def call_api(config_args: Dict[str, Any], messages: List[Dict[str, str]]) -> Optional[str]:
    """调用 AI 模型 API。
    Calls the AI model API.

    Args:
        config_args (Dict[str, Any]): 包含 API 配置的字典 (Dictionary with API configuration).
        messages (List[Dict[str, str]]): 待发送的消息列表 (List of messages to send).

    Returns:
        Optional[str]: AI 模型的原始响应文本，如果出错则返回 None。
                       The raw response text from the AI model, or None if an error occurs.
    """
    provider = config_args.get('model_provider')
    if not provider:
        print("AICli> 错误: 配置文件中未指定 'model_provider'。")
        return None

    try:
        client = APIClientFactory.get_api_client(provider, config_args)
        if client is None:
             print(f"AICli> 错误: 无法为提供商 '{provider}' 创建 API 客户端。可能是配置不完整或不支持。")
             return None

        print("AICli> 正在调用 AI 模型...") # Indicate API call start
        response = client.chat_completion(messages)
        print("AICli> 已收到 AI 模型响应。") # Indicate API call end
        return response
    except Exception as e:
        print(f"AICli> 错误: 调用 API 时出错 ({provider}): {e}")
        # Consider logging the full traceback here for debugging
        # import traceback
        # traceback.print_exc()
        return None
    finally:
        # 确保客户端资源被释放（如果需要）
        # Ensure client resources are released (if necessary)
        # 注意：如果客户端设计为可重用，则不应在这里关闭
        # Note: If the client is designed for reuse, it shouldn't be closed here
        if 'client' in locals() and hasattr(client, 'close'):
            try:
                client.close()
            except Exception as close_e:
                print(f"AICli> 警告: 关闭 API 客户端时出错: {close_e}")


def format_response(response: Optional[str]) -> Optional[Dict[str, Any]]:
    """解析和格式化 AI 模型的响应。
    Parses and formats the AI model's response.

    Args:
        response (Optional[str]): AI 模型的原始响应文本 (Raw response text from the AI model).

    Returns:
        Optional[Dict[str, Any]]: 解析后的结构化响应数据，如果解析失败或输入为 None 则返回 None。
                                 Parsed structured response data, or None if parsing fails or input is None.
    """
    if response is None:
        print("AICli> 错误: 没有收到有效的 API 响应，无法格式化。")
        return None

    try:
        response_formatter = DataFormatter(response)
        response_dict = response_formatter.parse()
        if response_dict is None:
             print("AICli> 错误: 无法从 AI 响应中解析出有效的 JSON 数据。")
             print("AICli> 原始响应内容:")
             print("--- Start of Raw Response ---")
             print(response)
             print("--- End of Raw Response ---")
             return None
        return response_dict
    except Exception as e:
        print(f"AICli> 错误: 格式化响应时出错: {e}")
        print("AICli> 原始响应内容:")
        print("--- Start of Raw Response ---")
        print(response)
        print("--- End of Raw Response ---")
        # Consider logging the full traceback here
        return None

def safe_execution(model_identifier: Optional[str], response_dict: Optional[Dict[str, Any]]) -> None:
    """安全地执行 AI 模型生成的命令。
    Safely executes commands generated by the AI model.

    Args:
        model_identifier (Optional[str]): 使用的 AI 模型标识符 (Identifier of the AI model used).
        response_dict (Optional[Dict[str, Any]]): 解析后的 AI 响应数据 (Parsed AI response data).
    """
    if response_dict is None:
        print("AICli> 错误: 没有有效的响应数据，无法执行命令。")
        return
    if not model_identifier:
         model_identifier = "Unknown Model" # Provide a default if missing

    try:
        exe = Execution(model_identifier, response_dict)
        exe.execute() # The execute method should handle user confirmation internally
    except Exception as e:
        print(f"AICli> 错误: 执行命令时出错: {e}")
        # Consider logging the full traceback here

def start_request(full_description: str) -> None:
    """处理用户请求的主流程。
    Main workflow for handling a user request.

    Args:
        full_description (str): 用户的完整输入描述 (User's full input description).
    """
    if not full_description or not full_description.strip():
        print("AICli> 请输入您想执行的操作描述。")
        return

    print(f"AICli> 收到请求: \"{full_description}\"")

    # 1. 加载配置
    print("AICli> 加载配置...")
    config_args: Dict[str, Any] = load_config()
    if not config_args:
        print("AICli> 错误: 无法加载配置。请检查 'config/default.yaml' 或活动配置文件。")
        return
    # 检查关键配置是否存在
    if not config_args.get('model_provider') or not config_args.get('model'):
         print(f"AICli> 错误: 当前配置文件 '{config_instance.get_active_profile()}' 中缺少 'model_provider' 或 'model'。")
         print(f"AICli> 请使用 'ai config update {config_instance.get_active_profile()}' 命令进行更新。")
         return

    # 2. 收集系统信息
    print("AICli> 收集系统信息...")
    system_args: Dict[str, Any] = load_system_info()

    # 3. 准备消息
    print("AICli> 准备发送给 AI 的消息...")
    messages: List[Dict[str, str]] = prepare_message(full_description, config_args, system_args)
    # print(f"DEBUG: Prepared messages: {messages}\n") # Uncomment for debugging

    # 4. 调用API获取结果
    response: Optional[str] = call_api(config_args, messages)
    # print(f"DEBUG: API response: {response}\n") # Uncomment for debugging

    # 5. 格式化返回结果
    if response:
        print("AICli> 正在解析 AI 响应...")
        response_dict: Optional[Dict[str, Any]] = format_response(response)
        # print(f"DEBUG: Formatted response: {response_dict}\n") # Uncomment for debugging

        # 6. 安全执行
        if response_dict:
            print("AICli> 准备打印响应结果...")
            safe_execution(config_args.get('model'), response_dict)
        else:
            print("AICli> 由于无法解析响应，未执行任何命令。")
    else:
        print("AICli> 未能从 AI 获取响应，无法继续。")
        return

    print("AICli> 请求处理完成。")


# --- Entry Point Example ---
if __name__ == '__main__':
    # --- 配置管理示例 ---
    # show_config()
    # list_all_profiles()
    # create_profile("my_new_test_profile") # Will prompt interactively
    # update_profile("my_new_test_profile") # Will prompt interactively
    # switch_config("my_new_test_profile")
    # delete_profile("my_new_test_profile") # Will ask for confirmation
    # switch_config("default")

    # --- 请求处理示例 ---
    print("\n" + "="*20 + " 开始处理请求 " + "="*20)
    start_request("显示当前目录下的所有文件和文件夹，包括隐藏文件，并按修改时间排序")
    print("="*20 + " 请求处理结束 " + "="*20 + "\n")

    # 示例：处理一个可能需要特定配置的请求
    # print("\n" + "="*20 + " 处理另一个请求 " + "="*20)
    # switch_config("your_preferred_profile") # Switch if needed
    # start_request("查找所有名为 'log.txt' 的文件")
    # print("="*20 + " 请求处理结束 " + "="*20 + "\n")
