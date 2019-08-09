import click
from iambic import app, db
from iambic.models import Post

@click.group()
def cli():
    pass


@click.command()
def initdb():
    click.echo("Creating Fresh Database")
    db.create_all()
    click.echo(f"Database Created at {app.config['SQLALCHEMY_DATABASE_URI']}")

@click.command()
@click.argument('body')
def add_post(body):
    click.echo("Adding Post")
    p = Post(body=body)
    db.session.add(p)
    db.session.commit()


cli.add_command(add_post)
cli.add_command(initdb)

if __name__ == '__main__':
    cli()