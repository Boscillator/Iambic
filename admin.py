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