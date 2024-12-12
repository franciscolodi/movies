from flask import Flask, request, redirect, url_for, render_template
import sqlite3

app = Flask(__name__)

# Crear la tabla si no existe
def init_db():
    with sqlite3.connect("app.db") as con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL
            )
        """)
        con.commit()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        comment = request.form["comment"]
        if comment:
            with sqlite3.connect("app.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO comments (content) VALUES (?)", (comment,))
                con.commit()
        return redirect(url_for("index"))
    
    # Leer todos los comentarios de la base de datos
    with sqlite3.connect("app.db") as con:
        cur = con.cursor()
        cur.execute("SELECT content FROM comments")
        comments = cur.fetchall()
    
    return render_template("index.html", comments=comments)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
