import click


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Weather Analytics Dashboard CLI."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
        # Implicit ctx.exit(0)
