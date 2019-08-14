import click
from iambic import create_app
from iambic.models import db, Post

@click.group()
def cli():
    pass


@click.command()
def initdb():
    click.echo("Creating Fresh Database")
    app = create_app('development')
    with app.app_context():
        db.create_all()

@click.command()
def run_debug():
    click.echo("Creating app...")
    app = create_app('development')
    click.echo("Running app...")
    app.run()


cli.add_command(run_debug)
cli.add_command(initdb)

if __name__ == '__main__':
    cli()