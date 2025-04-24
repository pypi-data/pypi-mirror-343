import click
from typing import Tuple, List, Any, Optional

# 假设 core 模块位于 ai_command_master 包中
# Assuming the core module is in the ai_command_master package
try:
    from ai_command_master import core
except ImportError:
    # 提供一个备选方案或更清晰的错误，以防模块路径问题
    # Provide a fallback or clearer error for module path issues
    print("Error: Failed to import 'core' module from 'ai_command_master'.")
    print("Please ensure the package is installed correctly and accessible.")
    import sys
    sys.exit(1)

# --- CLI Group Definition ---

@click.group(context_settings={
    # ignore_unknown_options: Allows passing options not defined by click.
    # Useful if the underlying core logic might handle them, but can hide typos.
    "ignore_unknown_options": True,
    # allow_extra_args: Allows arguments not associated with an option.
    # Crucial for the default 'ask' behavior.
    "allow_extra_args": True,
    # help_option_names: Standard help flags.
    "help_option_names": ['-h', '--help'],
    # terminal_width: Sets a fixed width for help messages for consistency.
    "terminal_width": 120
})
def cli() -> None:
    """
    ai-command-master: 通过自然语言生成并执行终端命令。
    (ai-command-master: Generate and execute terminal commands via natural language.)

    使用 'ai ask <您的描述>' 来与ai对话或生成命令。
    (Use 'ai ask <your description>' to generate commands.)

    使用 'ai config <subcommand>' 来管理配置。
    (Use 'ai config <subcommand>' to manage configurations.)
    """
    pass

# --- 'ask' Command ---

@cli.command(name="ask")
@click.argument('description', nargs=-1, required=True, type=click.STRING)
def ask_command(description: Tuple[str, ...]) -> None:
    """
    根据自然语言描述生成并执行命令。
    (Generates and executes commands based on a natural language description.)

    例如 (Example): ai ask 如何列出当前目录的文件
    """
    # 将捕获到的多个单词/参数合并成一个字符串
    # Join the captured words/arguments into a single string
    description_str: str = ' '.join(description)
    if not description_str:
        click.echo("AICli> 错误: 需要提供操作描述。 (Error: Description is required.)", err=True)
        # 显示 ask 命令的帮助信息
        # Show help for the ask command
        ctx = click.get_current_context()
        click.echo(ctx.get_help(), color=ctx.color)
        ctx.exit(1)
    try:
        core.start_request(description_str)
    except Exception as e:
        # 捕获调用核心逻辑时可能发生的意外错误
        # Catch unexpected errors when calling core logic
        click.echo(f"AICli> 执行请求时发生意外错误 (Unexpected error during request execution): {e}", err=True)
        # 可以在这里添加更详细的日志记录
        # More detailed logging could be added here

# --- 'config' Subgroup ---

@cli.group(name="config")
def config_group() -> None:
    """
    配置管理功能 (Configuration management functions)。

    管理不同的 AI 模型提供商和设置。
    (Manage different AI model providers and settings.)
    """
    pass

@config_group.command(name="show")
def show_config_command() -> None:
    """
    显示当前活动的配置文件。
    (Shows the currently active configuration profile.)
    """
    try:
        core.show_config()
    except Exception as e:
        click.echo(f"AICli> 显示配置时出错 (Error showing config): {e}", err=True)

@config_group.command(name="list")
def list_config_command() -> None:
    """
    列出所有可用的配置文件。
    (Lists all available configuration profiles.)
    """
    try:
        core.list_all_profiles()
    except Exception as e:
        click.echo(f"AICli> 列出配置时出错 (Error listing profiles): {e}", err=True)

@config_group.command(name="switch")
@click.argument('profile_name', type=click.STRING)
def switch_config_command(profile_name: str) -> None:
    """
    切换到指定的配置文件。
    (Switches to the specified configuration profile.)

    PROFILE_NAME: 要切换到的配置文件的名称。
                  (The name of the profile to switch to.)
    """
    if not profile_name:
         click.echo("AICli> 错误: 需要提供配置文件名称。(Error: Profile name is required.)", err=True)
         return
    try:
        core.switch_config(profile_name)
    except Exception as e:
        click.echo(f"AICli> 切换配置时出错 (Error switching profile): {e}", err=True)

@config_group.command(name="create")
@click.argument('profile_name', type=click.STRING)
def create_config_command(profile_name: str) -> None:
    """
    交互式地创建一个新的配置文件。
    (Interactively creates a new configuration profile.)

    PROFILE_NAME: 新配置文件的名称。
                  (The name for the new profile.)
    """
    if not profile_name:
         click.echo("AICli> 错误: 需要提供配置文件名称。(Error: Profile name is required.)", err=True)
         return
    try:
        core.create_profile(profile_name)
    except Exception as e:
        click.echo(f"AICli> 创建配置时出错 (Error creating profile): {e}", err=True)

@config_group.command(name="update")
@click.argument('profile_name', type=click.STRING, required=False)
def update_config_command(profile_name: Optional[str]) -> None:
    """
    交互式地更新指定的配置文件（如果未提供名称，则更新当前活动配置）。
    (Interactively updates the specified profile, or the active one if no name is given.)

    PROFILE_NAME: 要更新的配置文件的名称 (可选)。
                  (The name of the profile to update (optional).)
    """
    # core.update_profile 内部会处理 profile_name 为 None 的情况
    # The core.update_profile internally handles the case where profile_name is None
    try:
        core.update_profile(profile_name)
    except Exception as e:
        click.echo(f"AICli> 更新配置时出错 (Error updating profile): {e}", err=True)


@config_group.command(name="delete")
@click.argument('profile_name', type=click.STRING)
def delete_config_command(profile_name: str) -> None:
    """
    删除指定的配置文件。
    (Deletes the specified configuration profile.)

    PROFILE_NAME: 要删除的配置文件的名称。
                  (The name of the profile to delete.)
    """
    if not profile_name:
         click.echo("AICli> 错误: 需要提供配置文件名称。(Error: Profile name is required.)", err=True)
         return
    # core.delete_profile 内部包含确认步骤
    # The core.delete_profile includes a confirmation step internally
    try:
        core.delete_profile(profile_name)
    except Exception as e:
        click.echo(f"AICli> 删除配置时出错 (Error deleting profile): {e}", err=True)

# --- Default Command Handling ---

@cli.result_callback()
def handle_default_command(result: Any, **kwargs: Any) -> None:
    """
    处理默认行为：如果用户没有指定子命令 (如 'ask' 或 'config')，
    则将所有参数视为对 'ask' 命令的调用。
    (Handles the default behavior: if no subcommand like 'ask' or 'config'
    is specified, treat all arguments as an invocation of the 'ask' command.)
    """
    ctx = click.get_current_context(silent=True)
    # 检查是否有子命令被调用，以及是否有未被 click 处理的参数
    # Check if a subcommand was invoked and if there are unprocessed arguments
    if ctx and not ctx.invoked_subcommand and ctx.protected_args:
        # protected_args 包含命令名之后的第一个非选项参数
        # args 包含所有剩余的未被选项消耗的参数
        # protected_args contains the first non-option argument after the command name
        # args contains all remaining arguments not consumed by options
        description_parts: List[str] = list(ctx.protected_args) + list(ctx.args)
        description: str = ' '.join(description_parts)

        if description:
            # click.echo(f"DEBUG: No subcommand invoked, treating as 'ask' with description: '{description}'") # 用于调试
            try:
                core.start_request(description)
            except Exception as e:
                 click.echo(f"AICli> 执行默认请求时发生意外错误 (Unexpected error during default request execution): {e}", err=True)
            ctx.exit() # 成功处理后退出
        # else: 如果没有参数，click 通常会显示帮助信息，所以这里不需要处理

# --- Main Entry Point ---

if __name__ == '__main__':
    # 当脚本直接执行时，调用 click CLI 入口点
    # When the script is executed directly, call the click CLI entry point
    cli()
