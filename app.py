from flask import Flask, render_template, request, redirect
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 🔐 ADMIN PASSWORD
ADMIN_PASSWORD = "Delice@2026Secure!"

# 📁 UPLOAD FOLDER
UPLOAD_FOLDER = "static/images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 📦 DATA (temporaire)
posts = []

# -------------------
# 🌐 PAGE ACCUEIL
# -------------------
@app.route("/")
def home():
    category = request.args.get("category")

    if category:
        filtered = [p for p in posts if p["category"] == category]
    else:
        filtered = posts

    return render_template("index.html", posts=filtered)

# -------------------
# 🔐 ADMIN
# -------------------
@app.route("/admin-panel-9821", methods=["GET", "POST"])
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

        return redirect("/admin-panel-9821")

    return render_template("admin.html")

# -------------------
# 🛡️ ERREURS
# -------------------
@app.errorhandler(404)
def not_found(e):
    return "Page introuvable", 404

@app.errorhandler(500)
def server_error(e):
    return "Erreur serveur, réessayez plus tard", 500

# -------------------
# 🚀 LANCEMENT
# -------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)