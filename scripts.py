from atservices.scripts import make_data_cli, make_db_cli
from run import db, app


if __name__ == "__main__":
    with app.app_context():
        cli = make_data_cli(db=db)
        make_db_cli(cli=cli, db=db)
        cli()
