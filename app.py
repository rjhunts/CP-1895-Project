from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_session import Session
import os
import uuid

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
Session(app)

file_save_location = "static/images"
allowed_types = [".png", ".jpg", ".jpeg"]

@app.route("/", methods=["GET"])
def index():
    if "videoGames" not in session:
        print("clearing games")
        session["videoGames"] = []

    return render_template("index.html", games=session.get("videoGames"), file_location=file_save_location)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    elif request.method == "POST":
        if "videoGames" not in session:
            print("Clearing session data")
            session["videoGames"] = []
        title = request.form.get("gameTitle", "invalid")
        year = request.form.get("gameYear", "invalid")
        platform = request.form.get("gamePlatform", "invalid")
        desc = request.form.get("gameDescription", "invalid")
        uploaded_file = request.files["gameImage"]

        if uploaded_file.filename != '':
            extension = os.path.splitext(uploaded_file.filename)[1]
            if extension in allowed_types:
                unique_name = f"{uuid.uuid4().hex}{extension}"
                filename = os.path.join(file_save_location, unique_name)
                uploaded_file.save(filename)
                session["videoGames"].append({"title": title, "year": year, "platform": platform, "desc": desc, "image": unique_name})
            else:
                flash("The file is of the wrong type", "error")
                return redirect("./add")


        print(session.get("videoGames"))
        session.modified = True
        flash("Good job! You have added a new game to your collection", "message")
        return redirect("/")
    
@app.route("/remove", methods=["GET", "POST"])
def remove():
    if request.method == "GET":
        return render_template("remove.html", games=session.get("videoGames"), file_location=file_save_location)
    
    elif request.method == "POST":
        if "videoGames" not in session:
            session["videoGames"] = []

        remove = request.form.get("remove", "invalid")
        updated_games = []

        for game in session["videoGames"]:
            if remove == game["title"]:
                image_path = os.path.join(file_save_location, game["image"])
                if os.path.exists(image_path):
                    os.remove(image_path)
            else:
                updated_games.append(game)

        session["videoGames"] = updated_games
        session.modified = True
        return redirect("/")
