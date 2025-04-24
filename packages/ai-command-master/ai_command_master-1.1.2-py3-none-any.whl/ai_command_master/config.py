from typing import Dict, Any, Optional
import os
import yaml

class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self) -> None:
        """初始化配置管理器
        
        初始化配置管理器的各项属性，包括：
        - config_dir: 配置文件根目录
        - default_config: 默认配置文件路径
        - user_config_dir: 用户配置文件目录
        - active_profile: 当前激活的配置文件名
        - config_data: 配置数据字典
        """
        # 配置文件根目录
        self.config_dir: str = os.path.join(os.path.dirname(__file__), 'config')
        # 默认配置文件路径
        self.default_config: str = os.path.join(self.config_dir, 'default.yaml')
        # 用户配置文件目录
        self.user_config_dir: str = os.path.join(self.config_dir, 'profiles')
        # 最后使用的配置记录文件
        self.last_profile_file: str = os.path.join(self.config_dir, '.last_profile')
        # 确保配置目录存在
        os.makedirs(self.user_config_dir, exist_ok=True)
        # 初始化配置数据
        self.config_data: Dict[str, Any] = {}
        # 获取上次使用的配置
        self.active_profile: str = self._get_last_profile()
        # 加载配置
        self.load_config()

    def _get_last_profile(self) -> str:
        """获取上次使用的配置名称"""
        try:
            if os.path.exists(self.last_profile_file):
                with open(self.last_profile_file, 'r', encoding='utf-8') as f:
                    last_profile = f.read().strip()
                # 验证配置文件是否存在
                if last_profile and os.path.exists(os.path.join(self.user_config_dir, f"{last_profile}.yaml")):
                    return last_profile
        except Exception:
            pass
        return 'default'

    def _save_last_profile(self) -> None:
        """保存当前使用的配置名称
        
        使用文件锁确保多进程安全写入
        """
        try:
            with open(self.last_profile_file, 'w', encoding='utf-8') as f:
                # Windows系统使用 msvcrt 进行文件锁定
                import msvcrt
                msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
                try:
                    f.write(self.active_profile)
                    f.flush()  # 确保写入磁盘
                    os.fsync(f.fileno())  # 强制同步到磁盘
                finally:
                    # 释放锁
                    msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
        except Exception as e:
            # print(f"保存配置文件时出错: {str(e)}")
            pass
    def get_available_profiles(self) -> list:
        """获取所有可用的配置文件列表"""
        profiles: list = []
        for file in os.listdir(self.user_config_dir):
            if file.endswith('.yaml'):
                profiles.append(file[:-5])  # 移除.yaml后缀
        return profiles

    def create_profile(self, profile_name: str, config_data: Dict[str, Any] = None) -> bool:
        """创建新的配置文件
        Args:
            profile_name: 配置文件名称
            config_data: 配置数据，如果为None则复制当前配置
        """
        if not profile_name:
            raise ValueError("配置文件名称不能为空")
            
        profile_path = os.path.join(self.user_config_dir, f"{profile_name}.yaml")
        
        # 如果文件已存在，返回False
        if os.path.exists(profile_path):
            return False
            
        # 如果没有提供配置数据，使用当前配置
        if config_data is None:
            config_data = self.config_data

            
        # 写入新配置文件
        with open(profile_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(config_data, f, allow_unicode=True)

        # 自动切换当前配置文件
        self.active_profile = profile_name
        # 当前配置名写入文件
        self._save_last_profile()
        # 重加载配置文件
        self.load_config()
            
        return True

    def update_profile(self, profile_name: str) -> bool:
        """交互式更新配置文件
        Args:
            profile_name: 配置文件名称
        """
        profile_path = os.path.join(self.user_config_dir, f"{profile_name}.yaml")

        # 检查配置文件是否存在
        if not os.path.exists(profile_path):
            print(f"AICli> 配置文件 '{profile_name}' 不存在。")
            return False

        try:
            # 读取配置文件内容
            with open(profile_path, 'r', encoding='utf-8') as f:
                # 使用 safe_load 加载 YAML 数据
                dict_data = yaml.safe_load(f)
                # 如果文件为空或格式不正确，初始化为空字典
                if dict_data is None:
                    dict_data = {}

            # 定义需要交互式更新的配置项及其期望顺序
            # 注意：这里的顺序决定了向用户提问的顺序
            config_keys_in_order = ["model_provider", "model", "base_url", "api_key", "max_token", "temperature"]

            print(f"AICli> 开始更新配置文件 '{profile_name}' (按 Enter 跳过当前项):")

            # 创建一个副本用于存储可能更新的数据
            updated_data = dict_data.copy()
            has_changes = False # 标记是否有任何更改

            # 按照预定顺序遍历配置项
            for key in config_keys_in_order:
                # 获取当前值，如果键不存在则为 None
                current_value = updated_data.get(key)
                display_value = current_value if current_value is not None else "未设置" # 用于显示的值

                # 对 API Key 进行脱敏处理
                if key == "api_key" and isinstance(current_value, str) and len(current_value) > 8:
                    display_value = f"{current_value[:4]}...{current_value[-4:]}"
                elif current_value is None:
                     display_value = "未设置" # 明确显示未设置

                # 提示用户输入新值
                prompt_text = f"  {key} [{display_value}]: "
                try:
                    new_value_str = input(prompt_text).strip()
                except EOFError: # 处理管道或重定向输入结束的情况
                    print("\nAICli> 检测到输入结束，停止更新。")
                    break # 提前退出循环

                # 如果用户输入了内容，则处理并更新值
                if new_value_str:
                    # 对特定键进行类型转换
                    if key == "max_token":
                        try:
                            new_value = int(new_value_str)
                        except ValueError:
                            print(f"    输入无效，'{key}' 需要一个整数。保留原值 '{current_value}'。")
                            continue # 跳过此项更新
                    elif key == "temperature":
                        try:
                            new_value = float(new_value_str)
                            if not (0.0 <= new_value <= 2.0): # 假设温度范围
                                print(f"    输入无效，'{key}' 应在 0.0 到 2.0 之间。保留原值 '{current_value}'。")
                                continue
                        except ValueError:
                            print(f"    输入无效，'{key}' 需要一个浮点数。保留原值 '{current_value}'。")
                            continue
                    else:
                        # 其他键直接使用字符串值
                        new_value = new_value_str

                    # 只有当新值与旧值不同时才标记为更改
                    if updated_data.get(key) != new_value:
                        updated_data[key] = new_value
                        has_changes = True
                # 如果用户未输入 (按 Enter)，则不进行任何操作，保留原值

            # 只有在检测到更改时才写回文件
            if has_changes:
                try:
                    # 将更新后的配置写回文件
                    with open(profile_path, 'w', encoding='utf-8') as f:
                        # allow_unicode=True 支持中文等字符
                        # sort_keys=False 尝试保持原有顺序（对 PyYAML 效果有限）
                        yaml.safe_dump(updated_data, f, allow_unicode=True, sort_keys=False)
                    print(f"AICli> 配置文件 '{profile_name}' 更新成功。")

                    # 如果更新的是当前激活的配置，需要重新加载以使更改生效
                    if profile_name == self.active_profile:
                        print("AICli> 当前活动配置已更新，正在重新加载...")
                        self.load_config() # 重新加载配置

                except Exception as write_e:
                     print(f"AICli> 写入配置文件 '{profile_path}' 时出错: {str(write_e)}")
                     return False # 写入失败
            else:
                print(f"AICli> 未检测到任何更改，配置文件 '{profile_name}' 未被修改。")

            return True # 更新流程完成（无论是否有更改）

        except yaml.YAMLError as e:
            print(f"AICli> 解析配置文件 '{profile_path}' 时发生 YAML 错误: {str(e)}")
            return False
        except FileNotFoundError:
             print(f"AICli> 配置文件 '{profile_path}' 未找到。") # 理论上前面已检查，但以防万一
             return False
        except Exception as e:
            print(f"AICli> 更新配置文件 '{profile_name}' 时发生未知错误: {str(e)}")
            return False

    def switch_profile(self, profile_name: str) -> bool:
        """切换到指定的配置文件
        Args:.
            profile_name: 配置文件名称
        """
        profile_path = os.path.join(self.user_config_dir, f"{profile_name}.yaml")

        if not os.path.exists(profile_path):
            # 提示用户配置文件不存在
            print(f'AICli> 错误：无法切换，配置文件 "{profile_name}" 不存在。')
            # 列出可用的配置文件供用户参考
            available = self.get_available_profiles()
            if available:
                print(f"AICli> 可用的配置文件有: {', '.join(available)}")
            else:
                print("AICli> 当前没有可用的用户配置文件。")
            return False

        self.active_profile = profile_name
        # 当前配置名写入文件
        self._save_last_profile()
        # 切换后立即重新加载配置
        print(f"AICli> 已切换到配置文件: '{profile_name}'")
        self.load_config() # 加载新切换的配置
        return True

    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""

        # 如果用户配置文件目录为空，则创建用户配置文件目录
        if not os.path.exists(self.user_config_dir):
            os.makedirs(self.user_config_dir)

        try:
            # 首先加载默认配置
            with open(self.default_config, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f) or {}

            # 如果不是default配置，则加载对应的配置文件
            if self.active_profile != 'default':
                profile_path = os.path.join(self.user_config_dir, f"{self.active_profile}.yaml")
                if os.path.exists(profile_path):
                    with open(profile_path, 'r', encoding='utf-8') as f:
                        user_config = yaml.safe_load(f) or {}
                        # 深度合并配置
                        config_data = self._deep_merge(config_data, user_config)

            self.config_data = config_data
            return self.config_data
            
        except Exception as e:
            print(f"加载配置文件时出错: {str(e)}")
            return {}

    def _deep_merge(self, dict1: dict, dict2: dict) -> dict:
        """深度合并两个字典"""
        result = dict1.copy()
        for key, value in dict2.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    def get_config(self, key: str = None) -> Any:
        """获取配置值"""
        if key is None:
            return self.config_data
        
        keys = key.split('.')
        value = self.config_data
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return None
        return value

    def get_active_profile(self) -> str:
        """获取当前激活的配置文件名称"""
        return self.active_profile

    def delete_profile(self, profile_name: str) -> bool:
        """删除配置文件"""
        profile_path = os.path.join(self.user_config_dir, f"{profile_name}.yaml")
        try:
            # 检查文件是否存在
            if not os.path.exists(profile_path):
                return False
            # 如果删除的是当前文件，则切换到默认配置
            if profile_name == self.active_profile:
                self.switch_profile('default')
            # 删除文件
            os.remove(profile_path)
            print(f'AICli> 当前用户配置文件已被删除，自动切换到默认配置文件。')
        except Exception as e:
            print(f"AICli> 删除配置文件时出错: {str(e)}")

        return True
