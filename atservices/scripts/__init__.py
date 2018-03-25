import click
from .collatinus import download_collatinus_corpora, \
                        collatinus_corpora, \
                        check_collatinus_corpora, \
                        ingest_collatinus_corpora


def make_db_cli(cli=None, db=None):
    """ Toolbelt for database

    :param cli: Current click group
    :param db: Database to use
    :type db: flask_sqlalchemy.
    :return: Click instance
    """
    if cli is None:
        @click.group()
        def cli():
            pass

    @click.command("db-create")
    def create_db():
        click.echo("Creating database")
        db.create_all()

    @click.command("db-drop")
    def drop_db():
        click.echo("Dropping database")
        db.drop_all()

    @click.command("db-recreate")
    def recreate_db():
        click.echo("Recreating the database")
        db.drop_all()
        db.create_all()

    cli.add_command(create_db)
    cli.add_command(drop_db)
    cli.add_command(recreate_db)

    return cli


def make_data_cli(cli=None, db=None):
    """ Creates a data CommandLine Interface
    """
    if cli is None:
        @click.group()
        def cli():
            pass

    @click.command("data-download")
    @click.option("--force", is_flag=True, help="Force download the resources")
    def download(force=False):
        click.echo('Downloading Collatinus corpora')
        if force or check_collatinus_corpora():
            download_collatinus_corpora(click)

    @click.command("data-ingest")
    # @click.option("--clear", is_flag=True, help="Force download the resources")
    def ingest():
        ingest_collatinus_corpora(click)

    cli.add_command(download)
    cli.add_command(ingest)
    return cli


def make_data_survey_cli(cli=None, db=None):
    return cli