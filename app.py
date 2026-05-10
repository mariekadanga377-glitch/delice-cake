from flask import Flask, render_template, request, redirect
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

ADMIN_PASSWORD = "1234"

UPLOAD_FOLDER = "static/images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

posts = []

@app.route("/")
def home():
    category = request.args.get("category")

    if category:
        filtered = [p for p in posts if p["category"] == category]
    else:
        filtered = posts

    return render_template("index.html", posts=filtered, all_posts=posts)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":

        if request.form.get("password") != ADMIN_PASSWORD:
            return "❌ mot de passe incorrect"

        file = request.files["image"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        posts.append({
            "image": filename,
            "desc": request.form.get("desc"),
            "whatsapp": request.form.get("whatsapp"),
            "category": request.form.get("category"),
            "price": request.form.get("price")
        })

        return redirect("/admin")

    return render_template("admin.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)