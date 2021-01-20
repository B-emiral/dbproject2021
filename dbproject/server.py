from flask import Flask, render_template

import views
import database


def create_app(): 
    app = Flask(__name__)


    #If you want the data to be permanent, after running server.py once, please comment the line below. Otherwise, every time server.py is restarted, the database will become initial positon and the users you have created and their data will be lost.
    database.database_init()

    app.config.from_object("settings")
    app.secret_key = "secret_key"

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/course/<course_code>", view_func=views.transcript_page)
    app.add_url_rule("/curriculum", view_func=views.catalogterm_page)
    app.add_url_rule("/mapout", view_func=views.mapout_page, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=views.logout, methods=["GET"])
    app.add_url_rule("/login", view_func=views.login_page, methods=["GET","POST"])
    app.add_url_rule("/signup", view_func=views.signup_page, methods=["GET","POST"])
    app.add_url_rule("/editing", view_func=views.editing_page, methods=["POST"])
    app.add_url_rule("/account", view_func=views.account, methods=["POST"])
    
    return app



if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 3333)
    app.run(host="0.0.0.0", port=port, debug=True)