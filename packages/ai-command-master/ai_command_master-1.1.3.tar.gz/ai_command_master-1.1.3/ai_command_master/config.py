import os
import yaml
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

# 尝试导入 fcntl 用于 Unix/Linux 文件锁
try:
    import fcntl
    HAS_FCNTL = True
except ImportError:
    HAS_FCNTL = False

# 尝试导入 msvcrt 用于 Windows 文件锁
try:
    import msvcrt
    HAS_MSVCRT = True
except ImportError:
    HAS_MSVCRT = False

class ConfigManager:
    """
    一个单例模式的配置管理器，用于加载、管理和切换 YAML 配置文件。

    Attributes:
        config_dir (Path): 配置文件的根目录。
        default_config_path (Path): 默认配置文件的完整路径。
        user_config_dir (Path): 用户特定配置文件的目录。
        last_profile_file (Path): 存储最后使用的配置文件名称的文件路径。
        active_profile (str): 当前激活的配置文件名称（不含扩展名）。
        config_data (Dict[str, Any]): 加载后的配置数据字典。
    """
    _instance: Optional['ConfigManager'] = None

    def __new__(cls, *args, **kwargs) -> 'ConfigManager':
        """实现单例模式。"""
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            # 初始化只进行一次
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        """
        初始化配置管理器。

        设置路径，确保目录存在，加载初始配置。
        """
        # 使用 pathlib 处理路径
        base_dir = Path(__file__).parent
        self.config_dir: Path = base_dir / 'config'
        self.default_config_path: Path = self.config_dir / 'default.yaml'
        self.user_config_dir: Path = self.config_dir / 'profiles'
        self.last_profile_file: Path = self.config_dir / '.last_profile'

        # 确保配置目录存在
        self.user_config_dir.mkdir(parents=True, exist_ok=True)

        # 初始化配置数据
        self.config_data: Dict[str, Any] = {}

        # 获取上次使用的配置，如果不存在或无效则默认为 'default'
        self.active_profile: str = self._get_last_profile()

        # 加载配置
        self.load_config()

    def _get_last_profile(self) -> str:
        """
        获取上次使用的配置文件名称。

        从 .last_profile 文件读取。如果文件不存在、为空或对应的 profile 文件不存在，
        则返回 'default'。

        Returns:
            str: 上次使用的或默认的配置文件名称。
        """
        default_profile = 'default'
        if not self.last_profile_file.exists():
            return default_profile

        try:
            with open(self.last_profile_file, 'r', encoding='utf-8') as f:
                last_profile = f.read().strip()

            if not last_profile:
                return default_profile

            # 验证对应的 profile 文件是否存在
            profile_path = self.user_config_dir / f"{last_profile}.yaml"
            if profile_path.exists():
                return last_profile
            else:
                print(f"AICli> 警告: 上次使用的配置文件 '{last_profile}' 不再存在，将使用默认配置。")
                print(f"AICli> 注意: 默认配置文件 'default' 是只读的模板文件，请及时切换到其他配置文件。")
                # 如果上次的 profile 文件没了，也应该清除记录或指向 default
                self._save_profile_name(default_profile) # 更新 .last_profile 指向 default
                return default_profile
        except OSError as e:
            print(f"AICli> 警告: 读取最后使用的配置文件失败 ({self.last_profile_file}): {e}，将使用默认配置。")
            return default_profile
        except Exception as e:
            print(f"AICli> 警告: 处理最后使用的配置文件时发生未知错误: {e}，将使用默认配置。")
            return default_profile

    def _save_profile_name(self, profile_name: str) -> None:
        """
        将指定的配置文件名称保存到 .last_profile 文件。

        尝试使用平台特定的文件锁来保证写入的原子性。

        Args:
            profile_name (str): 要保存的配置文件名称。
        """
        try:
            # 使用 'w' 模式打开文件，如果文件存在则覆盖，不存在则创建
            with open(self.last_profile_file, 'w', encoding='utf-8') as f:
                # 尝试获取文件锁
                locked = False
                try:
                    if HAS_FCNTL:
                        fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                        locked = True
                    elif HAS_MSVCRT:
                        # msvcrt.locking 需要文件句柄，并且需要指定锁定的字节数
                        # 这里我们锁定整个文件（虽然只写少量数据），使用 1 字节作为象征
                        f.seek(0)
                        msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
                        locked = True

                    # 写入数据
                    f.write(profile_name)
                    f.flush()  # 确保内容写入缓冲区
                    os.fsync(f.fileno()) # 确保缓冲区内容写入磁盘

                except (IOError, OSError) as lock_e:
                     # 如果获取锁失败 (例如，在不支持锁的文件系统或已被锁定时)
                     # 仍然尝试写入，但在多进程场景下可能不安全
                     print(f"AICli> 警告: 无法锁定 .last_profile 文件 ({lock_e})，继续写入...")
                     f.seek(0) # 回到文件开头
                     f.truncate() # 清空文件以防旧内容残留
                     f.write(profile_name)
                     f.flush()
                     os.fsync(f.fileno())
                finally:
                    # 释放锁
                    if locked:
                        if HAS_FCNTL:
                            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                        elif HAS_MSVCRT:
                            f.seek(0)
                            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)

        except OSError as e:
            print(f"AICli> 错误: 保存最后使用的配置文件名失败 ({self.last_profile_file}): {e}")
        except Exception as e:
            print(f"AICli> 错误: 保存最后使用的配置文件名时发生未知错误: {e}")

    def _save_last_profile(self) -> None:
        """将当前激活的配置文件名称保存到 .last_profile 文件。"""
        self._save_profile_name(self.active_profile)

    def get_available_profiles(self) -> List[str]:
        """
        获取所有可用的用户配置文件列表（不含扩展名）。

        Returns:
            List[str]: 可用的配置文件名称列表。
        """
        profiles: List[str] = []
        if self.user_config_dir.exists() and self.user_config_dir.is_dir():
            for file_path in self.user_config_dir.glob('*.yaml'):
                profiles.append(file_path.stem) # .stem 获取不带后缀的文件名
        return sorted(profiles) # 返回排序后的列表

    def create_profile(self, profile_name: str, config_data: Optional[Dict[str, Any]] = None) -> bool:
        """
        创建新的配置文件。

        如果 config_data 为 None，则复制当前加载的配置（合并了默认配置和当前活动配置）。

        Args:
            profile_name (str): 新配置文件的名称（不含扩展名）。
            config_data (Optional[Dict[str, Any]]): 要写入新配置的数据。默认为 None。

        Returns:
            bool: 如果创建成功返回 True，如果文件已存在或发生错误返回 False。

        Raises:
            ValueError: 如果 profile_name 为空。
        """
        if not profile_name or not profile_name.strip():
            raise ValueError("配置文件名称不能为空")
        if profile_name == 'default':
             print(f"AICli> 错误: 不能创建名为 'default' 的配置文件，它是保留名称。")
             return False

        profile_path = self.user_config_dir / f"{profile_name}.yaml"

        if profile_path.exists():
            print(f"AICli> 错误: 配置文件 '{profile_name}' 已存在。")
            return False

        data_to_save = config_data if config_data is not None else self.config_data

        try:
            with open(profile_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(data_to_save, f, allow_unicode=True, sort_keys=False)
            print(f"AICli> 成功创建配置文件: '{profile_name}'")
            # 创建成功后，自动切换到新配置
            return self.switch_profile(profile_name)
        except yaml.YAMLError as e:
            print(f"AICli> 错误: 写入 YAML 数据到 '{profile_path}' 时出错: {e}")
            # 尝试删除可能已创建的不完整文件
            if profile_path.exists():
                try:
                    profile_path.unlink()
                except OSError:
                    pass # 删除失败也无能为力
            return False
        except OSError as e:
            print(f"AICli> 错误: 创建配置文件 '{profile_path}' 时发生文件系统错误: {e}")
            return False
        except Exception as e:
            print(f"AICli> 错误: 创建配置文件时发生未知错误: {e}")
            return False

    def update_profile(self, profile_name: str) -> bool:
        """
        交互式更新指定的配置文件。

        Args:
            profile_name (str): 要更新的配置文件名称（不含扩展名）。

        Returns:
            bool: 如果更新流程成功（无论是否有更改）返回 True，否则返回 False。
        """
        if profile_name == 'default':
            print("AICli> 提示: 'default' 配置文件是只读的模板，不能直接更新。")
            print("AICli> 如需修改默认设置，请编辑 'config/default.yaml' 文件。")
            print("AICli> 如需创建自定义配置，请使用 'create' 命令。")
            return False

        profile_path = self.user_config_dir / f"{profile_name}.yaml"

        if not profile_path.exists():
            print(f"AICli> 错误: 配置文件 '{profile_name}' 不存在。无法更新。")
            return False

        try:
            # 读取现有配置
            with open(profile_path, 'r', encoding='utf-8') as f:
                try:
                    current_data = yaml.safe_load(f) or {}
                except yaml.YAMLError as load_e:
                    print(f"AICli> 错误: 解析配置文件 '{profile_path}' 失败: {load_e}")
                    print(f"AICli> 请检查文件格式是否为有效的 YAML。")
                    return False

            # 定义需要交互式更新的配置项及其顺序和提示信息
            config_items = [
                {"key": "model_provider", "prompt": "模型提供商 (例如: openai, google, ollama)", "type": str},
                {"key": "model", "prompt": "模型名称 (例如: gpt-4, gemini-pro, llama3)", "type": str},
                {"key": "base_url", "prompt": "API 基地址 (留空则使用默认)", "type": str},
                {"key": "api_key", "prompt": "API 密钥 (敏感信息，将部分隐藏)", "type": str},
                {"key": "max_token", "prompt": "最大 Token 数 (整数)，最大值8192", "type": int},
                {"key": "temperature", "prompt": "温度 (0.0 到 1.0 之间的浮点数)", "type": float}
            ]

            print(f"\nAICli> === 开始更新配置文件 '{profile_name}' ===")
            print("AICli> (直接按 Enter 键将保留当前值)")

            updated_data = current_data.copy()
            has_changes = False

            for item in config_items:
                key = item["key"]
                prompt_text_base = item["prompt"]
                expected_type = item["type"]

                current_value = updated_data.get(key)
                display_value = str(current_value) if current_value is not None else "未设置"

                # 对 API Key 进行脱敏处理
                if key == "api_key" and isinstance(current_value, str) and len(current_value) > 8:
                    display_value = f"{current_value[:4]}...{current_value[-4:]}"

                prompt = f"  -> {prompt_text_base} [{display_value}]: "

                try:
                    raw_input = input(prompt).strip()
                except EOFError:
                    print("\nAICli> 检测到输入结束，停止更新。")
                    break # 提前退出循环

                if raw_input: # 用户输入了内容
                    try:
                        if expected_type == int:
                            new_value = int(raw_input)
                        elif expected_type == float:
                            new_value = float(raw_input)
                            # 添加范围检查示例
                            if key == "temperature" and not (0.0 <= new_value <= 2.0):
                                print(f"     警告: 温度值 '{new_value}' 超出建议范围 (0.0-2.0)。")
                                # 可以选择是接受还是拒绝，这里暂时接受
                        else: # str 类型
                             # 如果输入是 "none" 或 "null" (不区分大小写)，视为空值
                            if raw_input.lower() in ["none", "null"]:
                                 new_value = None
                            else:
                                new_value = raw_input

                        # 检查值是否真的改变了
                        if updated_data.get(key) != new_value:
                             # 如果新值是None，表示用户想删除这个键
                             if new_value is None and key in updated_data:
                                 del updated_data[key]
                                 print(f"     - 配置项 '{key}' 已移除。")
                                 has_changes = True
                             elif new_value is not None:
                                 updated_data[key] = new_value
                                 print(f"     + 配置项 '{key}' 更新为: {new_value}")
                                 has_changes = True

                    except ValueError:
                        print(f"     错误: 输入的值 '{raw_input}' 无法转换为所需的类型 ({expected_type.__name__})。保留原值。")
                        continue # 跳过此项更新
                # else: 用户按 Enter，不作修改

            print(f"AICli> === 更新结束 ===")

            # 只有在检测到更改时才写回文件
            if has_changes:
                try:
                    with open(profile_path, 'w', encoding='utf-8') as f:
                        yaml.safe_dump(updated_data, f, allow_unicode=True, sort_keys=False)
                    print(f"AICli> 配置文件 '{profile_name}' 更新成功。")

                    # 如果更新的是当前激活的配置，需要重新加载
                    if profile_name == self.active_profile:
                        print("AICli> 当前活动配置已更新，正在重新加载...")
                        self.load_config() # 重新加载配置

                except yaml.YAMLError as write_yaml_e:
                    print(f"AICli> 错误: 将更新后的配置写入 '{profile_path}' 时发生 YAML 错误: {write_yaml_e}")
                    return False
                except OSError as write_os_e:
                    print(f"AICli> 错误: 写入配置文件 '{profile_path}' 时发生文件系统错误: {write_os_e}")
                    return False
                except Exception as write_e:
                     print(f"AICli> 错误: 写入配置文件时发生未知错误: {write_e}")
                     return False
            else:
                print(f"AICli> 未检测到任何更改，配置文件 '{profile_name}' 未被修改。")

            return True # 更新流程完成

        except FileNotFoundError:
             # 理论上已在开头检查，但为了健壮性再加一次
             print(f"AICli> 错误: 配置文件 '{profile_path}' 在处理过程中丢失。")
             return False
        except Exception as e:
            print(f"AICli> 更新配置文件 '{profile_name}' 时发生未知错误: {e}")
            import traceback
            traceback.print_exc() # 打印详细错误堆栈
            return False

    def switch_profile(self, profile_name: str) -> bool:
        """
        切换到指定的配置文件。

        Args:
            profile_name (str): 要切换到的配置文件名称（不含扩展名）。

        Returns:
            bool: 如果切换成功返回 True，否则返回 False。
        """
        if profile_name == self.active_profile:
            print(f"AICli> 已经是配置文件 '{profile_name}'，无需切换。")
            # 确保配置是最新的
            self.load_config()
            return True

        target_path: Path
        if profile_name == 'default':
            # 切换到默认配置是允许的，即使没有对应的 user profile 文件
            target_path = self.default_config_path # 用于后续加载逻辑判断
        else:
            target_path = self.user_config_dir / f"{profile_name}.yaml"

        # 对于非 default 配置，检查文件是否存在
        if profile_name != 'default' and not target_path.exists():
            print(f'AICli> 错误: 无法切换，配置文件 "{profile_name}" 不存在。')
            available = self.get_available_profiles()
            if available:
                print(f"AICli> 可用的配置文件有: default, {', '.join(available)}")
            else:
                print("AICli> 当前没有可用的用户配置文件 (除了 'default')。")
            return False

        # 更新活动配置名称
        self.active_profile = profile_name
        # 保存当前选择
        self._save_last_profile()
        # 加载新配置
        print(f"AICli> 已切换到配置文件: '{profile_name}'")
        self.load_config() # 加载新切换的配置
        return True

    def load_config(self) -> Dict[str, Any]:
        """
        加载配置。

        首先加载默认配置，然后如果活动配置不是 'default'，
        则加载用户特定的配置并进行深度合并。

        Returns:
            Dict[str, Any]: 加载并合并后的配置数据。如果加载失败则返回空字典。
        """
        loaded_config: Dict[str, Any] = {}

        # 1. 加载默认配置
        try:
            if self.default_config_path.exists():
                with open(self.default_config_path, 'r', encoding='utf-8') as f:
                    loaded_config = yaml.safe_load(f) or {}
            else:
                print(f"AICli> 警告: 默认配置文件 '{self.default_config_path}' 未找到。")
                loaded_config = {} # 从空配置开始
        except yaml.YAMLError as e:
            print(f"AICli> 错误: 解析默认配置文件 '{self.default_config_path}' 失败: {e}")
            loaded_config = {} # 出错时使用空配置
        except OSError as e:
            print(f"AICli> 错误: 读取默认配置文件 '{self.default_config_path}' 失败: {e}")
            loaded_config = {}
        except Exception as e:
            print(f"AICli> 错误: 加载默认配置时发生未知错误: {e}")
            loaded_config = {}


        # 2. 如果活动配置不是 'default'，加载并合并用户配置
        if self.active_profile != 'default':
            profile_path = self.user_config_dir / f"{self.active_profile}.yaml"
            if profile_path.exists():
                try:
                    with open(profile_path, 'r', encoding='utf-8') as f:
                        user_config = yaml.safe_load(f) or {}
                    # 深度合并用户配置到默认配置上
                    loaded_config = self._deep_merge(loaded_config, user_config)
                except yaml.YAMLError as e:
                    print(f"AICli> 错误: 解析用户配置文件 '{profile_path}' 失败: {e}。将仅使用默认配置（如果可用）。")
                    # 不再合并，保留已加载的默认配置
                except OSError as e:
                    print(f"AICli> 错误: 读取用户配置文件 '{profile_path}' 失败: {e}。将仅使用默认配置（如果可用）。")
                except Exception as e:
                     print(f"AICli> 错误: 加载用户配置 '{self.active_profile}' 时发生未知错误: {e}。")
            else:
                # 这个情况理论上在 _get_last_profile 或 switch_profile 中已处理
                # 但为了健壮性，再次检查并警告
                print(f"AICli> 警告: 活动配置文件 '{self.active_profile}' 未找到。可能已被删除。")
                print(f"AICli> 将切换回 'default' 配置。")
                self.active_profile = 'default'
                self._save_last_profile()
                # 此时 loaded_config 仍然是默认配置的内容

        # 更新实例的配置数据
        self.config_data = loaded_config
        # print(f"AICli> 配置 '{self.active_profile}' 加载完成。") # 可以取消注释以获得更详细的日志
        return self.config_data

    def _deep_merge(self, base_dict: Dict[str, Any], merge_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        深度合并两个字典。merge_dict 的值会覆盖 base_dict 的值。

        Args:
            base_dict (Dict[str, Any]): 基础字典。
            merge_dict (Dict[str, Any]): 要合并进来的字典。

        Returns:
            Dict[str, Any]: 合并后的新字典。
        """
        result = base_dict.copy() # 从基础字典的浅拷贝开始
        for key, value in merge_dict.items():
            # 如果键同时存在于两个字典中，并且对应的都是字典，则递归合并
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            # 否则，直接用 merge_dict 的值覆盖（或添加）
            else:
                result[key] = value
        return result

    def get_config(self, key: Optional[str] = None, default: Any = None) -> Any:
        """
        获取配置值。支持点分表示法访问嵌套键。

        Args:
            key (Optional[str]): 要获取的配置键，例如 'database.host' 或 'model'。
                                 如果为 None，则返回整个配置字典。
            default (Any): 如果键不存在时返回的默认值。默认为 None。

        Returns:
            Any: 对应的配置值，或者如果键不存在则返回 default 值。
        """
        if key is None:
            return self.config_data

        keys = key.split('.')
        value = self.config_data
        try:
            for k in keys:
                # 检查 value 是否是字典以及 key 是否存在
                if isinstance(value, dict):
                    value = value[k]
                else:
                    # 如果在访问路径中遇到非字典类型，则无法继续深入
                    return default
            return value
        except KeyError:
            # 如果路径中的某个键不存在
            return default
        except TypeError:
             # 如果尝试在非字典对象上进行索引 (value[k])
             return default


    def get_active_profile(self) -> str:
        """获取当前激活的配置文件名称。"""
        return self.active_profile

    def delete_profile(self, profile_name: str) -> bool:
        """
        删除指定的用户配置文件。

        Args:
            profile_name (str): 要删除的配置文件名称（不含扩展名）。

        Returns:
            bool: 如果删除成功返回 True，如果文件不存在或删除失败返回 False。
        """
        if profile_name == 'default':
            print("AICli> 错误: 不能删除 'default' 配置文件。")
            return False

        profile_path = self.user_config_dir / f"{profile_name}.yaml"

        if not profile_path.exists():
            print(f"AICli> 错误: 配置文件 '{profile_name}' 不存在，无法删除。")
            return False

        try:
            # 先检查是否要删除当前活动的配置
            is_active = (profile_name == self.active_profile)

            # 删除文件
            profile_path.unlink()
            print(f"AICli> 成功删除配置文件: '{profile_name}'")

            # 如果删除的是当前活动的配置，则切换到 default
            if is_active:
                print(f"AICli> 当前活动的配置文件已被删除，自动切换到 'default' 配置。")
                print(f"AICli> 注意: 默认配置文件 'default' 是只读的模板文件，请及时切换其他配置文件。")
                self.switch_profile('default') # switch_profile 会处理加载和保存状态

            return True

        except OSError as e:
            print(f"AICli> 错误: 删除配置文件 '{profile_path}' 时发生文件系统错误: {e}")
            return False
        except Exception as e:
            print(f"AICli> 错误: 删除配置文件时发生未知错误: {e}")
            return False

# --- 示例用法 ---
if __name__ == "__main__":
    # 创建/获取 ConfigManager 实例 (单例)
    config_manager = ConfigManager()

    # 打印一些初始信息
    print(f"\n--- 配置管理器初始化完成 ---")
    print(f"配置文件根目录: {config_manager.config_dir}")
    print(f"默认配置文件: {config_manager.default_config_path}")
    print(f"用户配置目录: {config_manager.user_config_dir}")
    print(f"当前活动配置: {config_manager.get_active_profile()}")

    # 获取所有可用配置
    profiles = config_manager.get_available_profiles()
    print(f"可用用户配置: {profiles}")

    # 获取整个配置字典
    # print("\n当前完整配置:")
    # import json
    # print(json.dumps(config_manager.get_config(), indent=2, ensure_ascii=False))

    # 获取特定配置项
    print(f"\n获取模型配置: model = {config_manager.get_config('model', '未设置')}")
    print(f"获取嵌套配置: database.host = {config_manager.get_config('database.host', '未设置')}")
    print(f"获取不存在的配置: non_existent.key = {config_manager.get_config('non_existent.key', '这是默认值')}")

    # --- 交互式操作示例 (取消注释以运行) ---

    # # 1. 创建一个新配置 (如果 'my_test_profile' 不存在)
    # print("\n--- 尝试创建新配置 'my_test_profile' ---")
    # new_config_data = {
    #     "model_provider": "test_provider",
    #     "model": "test_model_v1",
    #     "api_key": "test_key_12345",
    #     "custom_setting": {"nested": True, "value": 100}
    # }
    # if config_manager.create_profile("my_test_profile", new_config_data):
    #     print(f"创建并切换到 'my_test_profile' 成功。当前活动配置: {config_manager.get_active_profile()}")
    #     print(f"新配置的 model: {config_manager.get_config('model')}")
    # else:
    #     print(f"创建 'my_test_profile' 失败或已存在。")
    #     # 如果创建失败但文件存在，可以尝试切换过去看看
    #     if "my_test_profile" in config_manager.get_available_profiles():
    #          config_manager.switch_profile("my_test_profile")
    #
    #
    # # 2. 交互式更新 'my_test_profile' (如果存在)
    # if "my_test_profile" in config_manager.get_available_profiles():
    #     print("\n--- 尝试更新配置 'my_test_profile' ---")
    #     config_manager.update_profile("my_test_profile")
    #     print(f"更新后 'my_test_profile' 的 model: {config_manager.get_config('model')}") # 如果更新的是活动配置，这里会显示新值
    # else:
    #      print("\n'my_test_profile' 不存在，跳过更新示例。")
    #
    #
    # # 3. 切换回 default 配置
    # print("\n--- 尝试切换回 'default' 配置 ---")
    # if config_manager.switch_profile("default"):
    #     print(f"切换回 'default' 成功。当前活动配置: {config_manager.get_active_profile()}")
    #     print(f"Default 配置的 model: {config_manager.get_config('model', '未设置')}")
    #
    #
    # # 4. 尝试删除 'my_test_profile' (如果存在)
    # if "my_test_profile" in config_manager.get_available_profiles():
    #      print("\n--- 尝试删除配置 'my_test_profile' ---")
    #      if config_manager.delete_profile("my_test_profile"):
    #          print(f"删除 'my_test_profile' 成功。")
    #          print(f"剩余可用用户配置: {config_manager.get_available_profiles()}")
    #          print(f"当前活动配置: {config_manager.get_active_profile()}") # 应该已切换回 default
    #      else:
    #          print(f"删除 'my_test_profile' 失败。")
    #
    # print("\n--- 示例结束 ---")
