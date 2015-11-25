# -*- coding: utf-8 -*-
from flask_assets import Bundle, Environment
from webassets.filter import register_filter
from webassets_browserify import Browserify

register_filter(Browserify)

css = Bundle(
    "libs/bootstrap/dist/css/bootstrap.css",
    "css/style.css",
    filters="cssmin",
    output="public/css/common.css"
)

js = Bundle(
    "libs/jQuery/dist/jquery.js",
    "libs/bootstrap/dist/js/bootstrap.js",
    "js/plugins.js",
    filters='jsmin',
    output="public/js/common.js"
)

dashboard_js_deps = Bundle(
    "libs/jQuery/dist/jquery.js",
    output="public/js/dashboard_libs.js"
)

overview_js = Bundle(
    "coffee/overview.coffee",
    filters=['coffeescript'],
    output="public/js/overview.js"
)

manage_js = Bundle(
    "coffee/manage.coffee",
    filters=['coffeescript'],
    output="public/js/manage.js"
)

manage_css = Bundle(
    "sass/manage.sass",
    filters=['sass'],
    output="public/css/manage.css"
)

admin_dash_css = Bundle(
    "sass/admin_dash.sass",
    filters=['sass'],
    output="public/css/admin_dash.css"
)


dashboard_css = Bundle(
    "sass/dashboard.sass",
    filters=['sass'],
    output="public/css/dashboard.css"
)

assets = Environment()

assets.register("js_all", js)
assets.register("css_all", css)
assets.register("dashboard_js_deps", dashboard_js_deps)
assets.register("overview_js", overview_js)
assets.register("manage_js", manage_js)
assets.register("dashboard_css", dashboard_css)
assets.register("manage_css", manage_css)
assets.register("admin_dash_css", admin_dash_css)
