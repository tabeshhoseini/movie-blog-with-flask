from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movie_blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(100))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.now)
    review = db.Column(db.Text)

    def __repr__(self):
        return f"movie : {self.title}  id : {self.id} "


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    movies = Movie.query.all()
    return render_template("index.html", movies=movies)


@app.route("/add")
def add_blog():
    return render_template("add.html")


@app.route("/submit_blog", methods=["POST"])
def submit_blog():
    title = request.form.get("movie_title")
    director = request.form.get("director")

    try:
        year = int(request.form.get("year", 0) or 0)
    except ValueError:
        year = None

    try:
        rating = float(request.form.get("rating", 0) or 0)
    except ValueError:
        rating = None

    review = request.form.get("review")

    new_movie = Movie(
        title=title, director=director, year=year, rating=rating, review=review
    )

    db.session.add(new_movie)
    db.session.commit()

    return redirect("/")


@app.route("/delete/<int:id>", methods=["POST"])
def delete_blog(id):
    movie = Movie.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/edit/<int:id>", methods=["GET"])
def edit_blog(id):
    movie = Movie.query.get_or_404(id)
    return render_template("edit.html", movie=movie)


@app.route("/update/<int:id>", methods=["POST"])
def update_blog(id):
    movie = Movie.query.get_or_404(id)

    movie.title = request.form.get("movie_title")
    movie.director = request.form.get("director")

    try:
        movie.year = int(request.form.get("year", 0) or 0)
    except ValueError:
        movie.year = None

    try:
        movie.rating = float(request.form.get("rating", 0) or 0)
    except ValueError:
        movie.rating = None

    movie.review = request.form.get("review")

    db.session.commit()

    return redirect(url_for("index"))


@app.route("/search")
def search():
    query = request.args.get("query", "")

    if query:
        movies = Movie.query.filter(
            (Movie.title.contains(query)) | (Movie.director.contains(query))
        ).all()
    else:
        movies = []

    return render_template("search.html", movies=movies, query=query)


if __name__ == "__main__":
    app.run()
