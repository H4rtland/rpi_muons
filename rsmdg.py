from flask import Flask
from flask import render_template
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup

from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
nav = Nav()
nav.init_app(app)


@nav.navigation()
def nav_bar_renderer():
    items = []
    items.append(View("Home", "index"))
    navbar = Navbar("rsmdg", *items)
    html = navbar.render()
    html = html.replace("navbar navbar-default", "navbar navbar-inverse navbar-fixed-top")
    navbar.render = lambda: html
    return navbar

@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
