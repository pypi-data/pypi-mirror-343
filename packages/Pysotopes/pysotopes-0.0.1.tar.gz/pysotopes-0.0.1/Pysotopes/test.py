from pysotopes import app, stylebook

styles = stylebook()

myApp = app(app_name = "my app", app_size = "400x400", style_book = styles)
widget = myApp.widgets()

@myApp.island
def mainApp():
    return [
        widget.text({"text" : "Hello world!"}, {"x" : 200, "y" : 200})
    ]

mainApp()

myApp.wrapUp()
