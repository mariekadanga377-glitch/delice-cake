from flask import Flask, render_template, request, redirect
import os
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 🔐 MOT DE PASSE ADMIN
ADMIN_PASSWORD = "Delice@2026Secure!"

# 📁 DOSSIER IMAGES
UPLOAD_FOLDER = "static/images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 💾 BASE DE DONNÉES
DATABASE = "database.db"

# -------------------------
# 🛠️ CREATION DATABASE
# -------------------------
def init_db():

    conn = sqlite3.connect(DATABASE)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image TEXT,
        description TEXT,
        category TEXT,
        price TEXT
    )
    """)

    conn.close()

init_db()

# -------------------------
# 🌐 PAGE ACCUEIL
# -------------------------
@app.route("/admin-panel-9821", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        if request.form.get("password") != ADMIN_PASSWORD:
            return "❌ mot de passe incorrect"

        file = request.files["image"]

        if file.filename == "":
            return "❌ aucune image sélectionnée"

        filename = secure_filename(file.filename)

        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        conn = sqlite3.connect(DATABASE)

        conn.execute(
            "INSERT INTO posts (image, description, category, price) VALUES (?, ?, ?, ?)",
            (
                filename,
                request.form.get("desc"),
                request.form.get("category"),
                request.form.get("price")
            )
        )

        conn.commit()
        conn.close()

        return redirect("/admin-panel-9821")

    return render_template("admin.html")

    category = request.args.get("category")

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    if category:
        posts = conn.execute(
            "SELECT * FROM posts WHERE category=?",
            (category,)
        ).fetchall()

    else:
        posts = conn.execute(
            "SELECT * FROM posts ORDER BY id DESC"
        ).fetchall()

    conn.close()

    return render_template("index.html", posts=posts)

# -------------------------
# 🔐 ADMIN
# -------------------------
@app.route("/admin-panel-9821", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        if request.form.get("password") != ADMIN_PASSWORD:
            return "❌ mot de passe incorrect"

        file = request.files["image"]

        filename = secure_filename(file.filename)

        file.save(os.path.join(UPLOAD_FOLDER, filename))

        desc = request.form.get("desc")
        category = request.form.get("category")
        price = request.form.get("price")

        conn = sqlite3.connect(DATABASE)

        conn.execute(
            "INSERT INTO posts (image, description, category, price) VALUES (?, ?, ?, ?)",
            (filename, desc, category, price)
        )

        conn.commit()
        conn.close()

        return redirect("/admin-panel-9821")

    return render_template("admin.html")

# -------------------------
# 🛡️ ERREURS
# -------------------------
@app.errorhandler(404)
def not_found(e):
    return "Page introuvable", 404

@app.errorhandler(500)
def server_error(e):
    return "Erreur serveur", 500

# -------------------------
# 🚀 LANCEMENT
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)