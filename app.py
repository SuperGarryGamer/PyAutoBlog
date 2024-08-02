import os
import json
import mistune
from flask import Flask, send_from_directory, render_template

post_indexes = {}

def create_app():
    update_indexes()
    app = Flask(__name__)

    @app.route("/")
    def root():
        print(post_indexes)
        return "<h1>Welcome to PyAutoBlog :3</h1>"

    @app.route("/favicon.ico")
    def favicon():
        return send_from_directory("./static", "favicon.ico")
    
    @app.route("/posts/<title>/")
    def send_post(title=None):
        if title not in post_indexes.values():
            return render_template("404.html"), 404
        meta = get_post_metadata(title)
        md_text = ""
        with open(f"posts/{title}/post.md") as f:
            md_text = f.read()
        
        return render_template("post.html", post_title = meta["post-title"], post_content=mistune.html(md_text))

    @app.route("/posts/<title>/<filename>")
    def send_post_file(title=None, filename=None):
        return send_from_directory(f"./posts/{title}", filename)

    return app    

def update_indexes():
    global post_indexes

    loaded_posts = {}
    posts = os.listdir("posts")
    for post in posts:
        metadata = get_post_metadata(post)
        loaded_posts[metadata["post-index"]] = post
    post_indexes = loaded_posts

def get_post_metadata(title):
    # breaks if title is wronk
    metadata = {}
    with open(f"posts/{title}/meta.json", "r") as f:
            metadata = json.load(f)
    return metadata
