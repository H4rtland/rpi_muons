from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Text, Separator

from app import app

nav = Nav()
nav.init_app(app)

@nav.navigation()
def nav_bar_renderer():
    items = []
    items.append(View("Home", "index"))
    items.append(View("Detector", "detector.detector_status"))
    items.append(View("Results", "result.result_list"))
    items.append(View("Log", "log"))
    navbar = Navbar("rsmdg", *items)
    html = navbar.render()
    html = html.replace("navbar navbar-default", "navbar navbar-inverse navbar-fixed-top")
    navbar.render = lambda: html
    return navbar