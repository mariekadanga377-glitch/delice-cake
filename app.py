import os
import sqlite3
from flask import Flask, render_template, request, redirect, session
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ================= CONFIG =================
app.secret_key = "delicecake_secret_final"

UPLOAD_FOLDER = "static/images"
DATABASE = "database.db"
ADMIN_PASSWORD = "1234"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ================= DATABASE =================
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
    conn.commit()
    conn.close()

init_db()

# ================= HOME =================
@app.route("/")
def index():
    category = request.args.get("category")

    conn = sqlite3.connect(DATABASE)

    if category:
        posts = conn.execute(
            "SELECT * FROM posts WHERE category=? ORDER BY id DESC",
            (category,)
        ).fetchall()
    else:
        posts = conn.execute(
            "SELECT * FROM posts ORDER BY id DESC"
        ).fetchall()

    conn.close()
    return render_template("index.html", posts=posts)

# ================= CAKE PAGE =================
@app.route("/cake/<int:id>")
def cake(id):
    conn = sqlite3.connect(DATABASE)
    cake = conn.execute("SELECT * FROM posts WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("cake.html", cake=cake)

# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/admin")
        return "❌ mot de passe incorrect"
    return render_template("login.html")

# ================= ADMIN =================
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("admin"):
        return redirect("/login")

    conn = sqlite3.connect(DATABASE)

    if request.method == "POST":
        file = request.files.get("image")

        if file and file.filename != "":
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

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

    posts = conn.execute("SELECT * FROM posts ORDER BY id DESC").fetchall()
    conn.close()

    return render_template("admin.html", posts=posts)

# ================= DELETE =================
@app.route("/delete/<int:id>")
def delete(id):
    if not session.get("admin"):
        return redirect("/login")

    conn = sqlite3.connect(DATABASE)
    conn.execute("DELETE FROM posts WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/admin")

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)