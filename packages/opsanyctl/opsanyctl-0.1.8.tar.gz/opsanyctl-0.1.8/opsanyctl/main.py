import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import typer
from rich.console import Console
from rich.table import Table
# from tabulate import tabulate
from rich.text import Text
from opsanyctl.api.resource_type import ResourceType
from opsanyctl.api.fields import ResourceFields
from opsanyctl.api.resource import Resource
from opsanyctl.help_content import *
from opsanyctl.libs import load_yaml_config, check_command

supported_commands = [
    "--help",
    "config",  # 获取配置文件
    "get",  # 获取各类资源数据
    "res",  # api-resources 简写
    "api-resources",  # 获取全部资源模型
]

app = typer.Typer(
    context_settings={"help_option_names": ["-h", "--help"]},
    # help=typer_help_content,
    add_completion=False
)

check_command(supported_commands)

console = Console()

config_status, opsanyctl_config = load_yaml_config()
if not config_status:
    typer.echo(typer.style(opsanyctl_config, fg=typer.colors.YELLOW, bold=True))
    sys.exit(1)

default_config = opsanyctl_config.get('config') or {}
default_resource_short = opsanyctl_config.get('resourceShort') or {}
resource_id_default_field = default_config.get('resourceIdDefaultField') or "code,VISIBLE_NAME,name"
resource_id_field_search = default_config.get('resourceIdFieldSearch') or False
resource_default_limit = default_config.get('resourceDefaultLimit') or 20
api_resources_default_limit = default_config.get('apiResourcesDefaultLimit') or 100


@app.command("config", help=command_config_help)
def config():
    typer.echo(typer.style(config_content_title, fg=typer.colors.GREEN, bold=True))
    typer.echo(config_content)


@app.command("api-resources", help=command_api_resources_help)
def api_resources(
        output: str = typer.Option("", "--output", "-o", help=command_api_resources_arg_output_help),
        limit: int = typer.Option(api_resources_default_limit, "--limit", "-l",
                                  help=command_api_resources_arg_limit_help)
):
    res = ResourceType(opsanyctl_config)
    status, headers, data, mess = res.get_resources_type(output, limit, default_short=default_resource_short)
    if not status:
        typer.echo(typer.style(mess, fg=typer.colors.YELLOW, bold=True))
        return
    table = Table(show_header=True, header_style="bold magenta", expand=False)
    for header in headers:
        table.add_column(header, no_wrap=False, overflow="fold")
    for row in data:
        table.add_row(*row)
    console.print(table)

@app.command("res", help=command_re_help)
def res(
        output: str = typer.Option("", "--output", "-o", help=command_api_resources_arg_output_help),
        limit: int = typer.Option(api_resources_default_limit, "--limit", "-l",
                                  help=command_api_resources_arg_limit_help)
):
    api_resources(output, limit)


@app.command("get", help=command_get_help)
def get(
        resource_type: str = typer.Argument(..., help=command_get_arg_resource_type_help),
        resource_id: str = typer.Argument(None, help=command_get_arg_resource_id_help),
        search: str = typer.Option(None, "--search", "-s", help=command_get_opt_search_help),
        fields: str = typer.Option(None, "--fields", "-f", help=command_get_opt_fields_help),
        page: int = typer.Option(1, "--page", "-p", help=command_get_opt_page_help),
        limit: int = typer.Option(resource_default_limit, "--limit", "-l", help=command_get_opt_limit_help)
):
    # ser ser.fields OPSANY_SAAS_VERSION OPSANY_SAAS_VERSION.fields
    if "." in resource_type:
        resource, field = resource_type.split(".")
    else:
        resource, field = resource_type, ""
    if resource in default_resource_short:
        resource = default_resource_short[resource]
    if field:
        if field == "fields":
            res = ResourceFields(opsanyctl_config)
            status, headers, data, mess = res.get_resource_field(resource)
        else:
            mess = f"当前资源 {resource} 不支持属性 {field}，请使用 {resource}.fields 等"
            typer.echo(typer.style(mess, fg=typer.colors.YELLOW, bold=True))
            return
    else:
        res = Resource(opsanyctl_config)
        status, headers, data, mess = res.get_resource(resource, resource_id, search, fields, page, limit,
                                                       resource_id_default_field, resource_id_field_search)
    if not status:
        typer.echo(typer.style(mess, fg=typer.colors.YELLOW, bold=True))
        return
    table = Table(show_header=True, header_style="bold magenta", expand=False)
    for header in headers:
        if isinstance(header, list):
            header_text = Text(justify="center")
            for h in header:
                header_text.append(h, style="bold magenta")
                header_text.append("\n")
        else:
            header_text = header
        table.add_column(header_text, no_wrap=False, overflow="fold")

    for row in data:
        table.add_row(*row)
    console.print(table)
    console.print(Text(mess, style="italic green"))


if __name__ == "__main__":
    # python main.py api-resources --help
    # python main.py get ser
    app()
