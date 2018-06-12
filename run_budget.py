from budget import create_app  # import the create_app function from the __init__.py module in the main budget package (folder)


app = create_app()  # create application
app.app_context().push()


if __name__ == '__main__':
    app.run(debug=True)  # debugger is active
