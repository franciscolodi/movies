from flask import Flask, request, redirect, url_for, render_template
import sqlite3

app = Flask(__name__)

# Crear la base de datos para las películas y comentarios
def init_db():
    with sqlite3.connect("movie.db") as con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                year INTEGER NOT NULL,
                director TEXT NOT NULL,
                description TEXT NOT NULL
            )
        """)
        con.commit()
    
    with sqlite3.connect("app.db") as con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                FOREIGN KEY (movie_id) REFERENCES movies (id)
            )
        """)
        con.commit()

# Ruta principal para mostrar películas y comentarios
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        movie_id = request.form["movie_id"]
        comment = request.form["comment"]
        if comment:
            with sqlite3.connect("app.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO comments (movie_id, content) VALUES (?, ?)", (movie_id, comment))
                con.commit()
        return redirect(url_for("index"))
    
    # Leer todas las películas de la base de datos
    with sqlite3.connect("movie.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM movies")
        movies = cur.fetchall()
    
    # Leer todos los comentarios de la base de datos
    with sqlite3.connect("app.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM comments")
        comments = cur.fetchall()

    return render_template("index.html", movies=movies, comments=comments)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
