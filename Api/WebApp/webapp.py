from flask import Blueprint, render_template, redirect, url_for, session, jsonify
from App.Middlewares.Database.MongoDB.file import middle_get_files
from App.Middlewares.Database.MongoDB.llm import middle_get_prompt
from App.Middlewares.Database.MongoDB.auth import middle_get_user

web = Blueprint("web", __name__, template_folder='templates')

@web.route("/signup")
def signup():
    return render_template("v1/signup.html")

@web.route("/login")
def login():

    if "user_token" in session:
        return redirect(url_for("web.home"))

    return render_template("v1/login.html")

@web.route("/home")
def home():
    if "user_token" not in session:
        return redirect(url_for("web.login"))

    return render_template("v1/home.html")

@web.route("/setting")
def setting():
    if "user_token" not in session:
        return redirect(url_for("web.login"))

    # Get user auth from database
    result = middle_get_user(user_token=session["user_token"])
        
    return render_template("v1/setting.html", user=result["data"])

@web.route("/LLM/setting")
def llm_setting():
    if "user_token" not in session:
        return redirect(url_for("web.login"))

    llm_prompt = middle_get_prompt({"user_token": session["user_token"]})

    if llm_prompt["status"] == 404:
        return render_template("v1/llm_setting.html", prompt=None)
    
    return render_template("v1/llm_setting.html", prompt=llm_prompt["data"]["prompt"], llm_configuration=llm_prompt["data"]["llm"], splitter_configuration=llm_prompt["data"]["splitter"])

@web.route("/file")
def file():
    if "user_token" not in session:
        return redirect(url_for("web.login"))
    
    files = middle_get_files(session["user_token"])

    return render_template("v1/file.html", result=files["data"])

@web.route("/")
def index():

    if "user_token" in session:
        return redirect(url_for("web.home"))

    return redirect(url_for("web.login"))