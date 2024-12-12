from flask import Flask, request, redirect, url_for, render_template
import sqlite3

app = Flask(__name__)

# Crear la tabla si no existe
def init_db():
    with sqlite3.connect("app.db") as con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS movie_comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_name TEXT NOT NULL,
                fecha DATE,
                comentarios_kpaz TEXT,
                comentarios_flodi TEXT
            )
        """)
        con.commit()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Obtener los datos del formulario
        movie_data = []
        for i in range(1, 24):  # Asumimos que hay 23 películas
            movie_name = request.form[f"movie{i}"]
            fecha = request.form[f"fecha{i}"]
            comentarios_kpaz = request.form[f"comentariosKPAZ{i}"]
            comentarios_flodi = request.form[f"comentariosFLODI{i}"]
            
            if movie_name and fecha:  # Si hay película y fecha, guardar los comentarios
                movie_data.append((movie_name, fecha, comentarios_kpaz, comentarios_flodi))
        
        if movie_data:
            with sqlite3.connect("app.db") as con:
                cur = con.cursor()
                cur.executemany("""
                    INSERT INTO movie_comments (movie_name, fecha, comentarios_kpaz, comentarios_flodi) 
                    VALUES (?, ?, ?, ?)
                """, movie_data)
                con.commit()
        
        return redirect(url_for("index"))
    
    # Leer todos los comentarios de la base de datos
    with sqlite3.connect("app.db") as con:
        cur = con.cursor()
        cur.execute("SELECT movie_name, fecha, comentarios_kpaz, comentarios_flodi FROM movie_comments")
        comments = cur.fetchall()

    return render_template("index.html", comments=comments)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
