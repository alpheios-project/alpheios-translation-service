from atservices import create_app


app, db = create_app()


if __name__ == "__main__":
    app.DEBUG = True
    app.run()