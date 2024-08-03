import os
import json
import mistune
import threading
import time
from flask import Flask, send_from_directory, render_template

post_indexes = {}

def create_app():
    update_indexes()
    index_thread = threading.Thread(target=update_indexes_repeatedly, daemon=True, args=(3600,))
    index_thread.start()
    app = Flask(__name__)

    @app.route("/")
    def root():
        print(post_indexes)
        return render_template("homepage.html", posts = get_last_n_posts(5))
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
        
        return render_template("post.html", post_title = meta["post-title"], post_date = meta["post-date"], post_content=mistune.html(md_text))

    @app.route("/posts/<title>/<filename>")
    def send_post_file(title=None, filename=None):
        return send_from_directory(f"./posts/{title}", filename)

    return app    

def update_indexes():
    global post_indexes

    print("Updating indexes...")
    loaded_posts = {}
    posts = os.listdir("posts")
    for post in posts:
        metadata = get_post_metadata(post)
        loaded_posts[metadata["post-index"]] = post
    post_indexes = loaded_posts
    print("Indexes updated :3")

def get_post_metadata(title):
    # breaks if title is wronk
    metadata = {}
    with open(f"posts/{title}/meta.json", "r") as f:
            metadata = json.load(f)
    return metadata

def update_indexes_repeatedly(interval):
    while True:
        time.sleep(interval)
        update_indexes()

def get_last_n_posts(n):
    num_to_fetch = n
    posts = []
    if len(post_indexes) < n:
        num_to_fetch = len(post_indexes)
    
    for i in range(num_to_fetch):
        title = post_indexes[len(post_indexes) - 1 - i] # Get i-th-newest post
        meta = get_post_metadata(title)
        posts.append({"title": title, "pretty_title": meta["post-title"], "date": meta["post-date"]})
    return posts
