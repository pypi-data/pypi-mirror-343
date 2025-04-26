"""
Utility commands for the CLI.
"""

import click
import json
from elastro.core.client import ElasticsearchClient
from elastro.utils.templates import TemplateManager
from elastro.utils.aliases import AliasManager
from elastro.utils.health import HealthCheck
from elastro.core.errors import OperationError

@click.command("health")
@click.option("--level", type=click.Choice(["cluster", "indices", "shards"]), default="cluster",
              help="Health check level")
@click.option("--wait", type=str, help="Wait for specified status (green, yellow, red)")
@click.option("--timeout", type=str, default="30s", help="Timeout for health check")
@click.pass_obj
def health(client, level, wait, timeout):
    """Check Elasticsearch cluster health."""
    health_check = HealthCheck(client)

    try:
        result = health_check.check(level=level, wait_for_status=wait, timeout=timeout)

        # Format output based on status
        status = result.get("status", "unknown")
        status_colors = {
            "green": "green",
            "yellow": "yellow",
            "red": "red"
        }

        click.echo(
            click.style(
                f"Cluster: {result.get('cluster_name', 'unknown')} | "
                f"Status: {status} | "
                f"Nodes: {result.get('number_of_nodes', 0)} | "
                f"Data nodes: {result.get('number_of_data_nodes', 0)}",
                fg=status_colors.get(status, "white")
            )
        )

        # Display additional info
        click.echo(json.dumps(result, indent=2))
    except OperationError as e:
        click.echo(f"Error checking health: {str(e)}", err=True)
        exit(1)

@click.group("templates")
def templates():
    """Manage index templates."""
    pass

@templates.command("list")
@click.option("--type", type=click.Choice(["index", "component"]), help="Template type")
@click.option("--name", type=str, help="Template name pattern")
@click.pass_obj
def list_templates(client, type, name):
    """List index templates."""
    template_manager = TemplateManager(client)

    try:
        result = template_manager.list(template_type=type, name=name)
        click.echo(json.dumps(result, indent=2))
    except OperationError as e:
        click.echo(f"Error listing templates: {str(e)}", err=True)
        exit(1)

@templates.command("get")
@click.argument("name", type=str)
@click.option("--type", type=click.Choice(["index", "component"]), default="index", help="Template type")
@click.pass_obj
def get_template(client, name, type):
    """Get an index template."""
    template_manager = TemplateManager(client)

    try:
        result = template_manager.get(name, template_type=type)
        click.echo(json.dumps(result, indent=2))
    except OperationError as e:
        click.echo(f"Error retrieving template: {str(e)}", err=True)
        exit(1)

@templates.command("create")
@click.argument("name", type=str)
@click.option("--file", type=click.Path(exists=True, readable=True), required=True, help="Template definition file")
@click.option("--type", type=click.Choice(["index", "component"]), default="index", help="Template type")
@click.pass_obj
def create_template(client, name, file, type):
    """Create an index template."""
    template_manager = TemplateManager(client)

    # Load template definition
    with open(file, 'r') as f:
        template_def = json.load(f)

    try:
        result = template_manager.create(name, template_def, template_type=type)
        click.echo(json.dumps(result, indent=2))
        click.echo(f"Template '{name}' created successfully.")
    except OperationError as e:
        click.echo(f"Error creating template: {str(e)}", err=True)
        exit(1)

@templates.command("delete")
@click.argument("name", type=str)
@click.option("--type", type=click.Choice(["index", "component"]), default="index", help="Template type")
@click.option("--force", is_flag=True, help="Force deletion without confirmation")
@click.pass_obj
def delete_template(client, name, type, force):
    """Delete an index template."""
    template_manager = TemplateManager(client)

    # Confirm deletion unless --force is provided
    if not force:
        confirm = click.confirm(f"Are you sure you want to delete template '{name}'?")
        if not confirm:
            click.echo("Operation cancelled.")
            return

    try:
        result = template_manager.delete(name, template_type=type)
        click.echo(json.dumps(result, indent=2))
        click.echo(f"Template '{name}' deleted successfully.")
    except OperationError as e:
        click.echo(f"Error deleting template: {str(e)}", err=True)
        exit(1)

@click.group("aliases")
def aliases():
    """Manage index aliases."""
    pass

@aliases.command("list")
@click.option("--index", type=str, help="Filter by index")
@click.option("--name", type=str, help="Filter by alias name")
@click.pass_obj
def list_aliases(client, index, name):
    """List index aliases."""
    alias_manager = AliasManager(client)

    try:
        result = alias_manager.list(index=index, name=name)
        click.echo(json.dumps(result, indent=2))
    except OperationError as e:
        click.echo(f"Error listing aliases: {str(e)}", err=True)
        exit(1)

@aliases.command("create")
@click.argument("name", type=str)
@click.argument("index", type=str)
@click.option("--is-write-index", is_flag=True, help="Set as write index")
@click.option("--routing", type=str, help="Routing value")
@click.option("--filter", type=str, help="Filter query (JSON string)")
@click.pass_obj
def create_alias(client, name, index, is_write_index, routing, filter):
    """Create an index alias."""
    alias_manager = AliasManager(client)

    # Parse filter if provided
    filter_query = None
    if filter:
        try:
            filter_query = json.loads(filter)
        except json.JSONDecodeError:
            click.echo("Error: Filter must be a valid JSON string", err=True)
            exit(1)

    try:
        result = alias_manager.create(
            name,
            index,
            is_write_index=is_write_index,
            routing=routing,
            filter=filter_query
        )
        click.echo(json.dumps(result, indent=2))
        click.echo(f"Alias '{name}' created for index '{index}'.")
    except OperationError as e:
        click.echo(f"Error creating alias: {str(e)}", err=True)
        exit(1)

@aliases.command("delete")
@click.argument("name", type=str)
@click.argument("index", type=str)
@click.option("--force", is_flag=True, help="Force deletion without confirmation")
@click.pass_obj
def delete_alias(client, name, index, force):
    """Delete an index alias."""
    alias_manager = AliasManager(client)

    # Confirm deletion unless --force is provided
    if not force:
        confirm = click.confirm(f"Are you sure you want to delete alias '{name}' from index '{index}'?")
        if not confirm:
            click.echo("Operation cancelled.")
            return

    try:
        result = alias_manager.delete(name, index)
        click.echo(json.dumps(result, indent=2))
        click.echo(f"Alias '{name}' deleted from index '{index}'.")
    except OperationError as e:
        click.echo(f"Error deleting alias: {str(e)}", err=True)
        exit(1)
