from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import (
    UserMixin,
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:8461@localhost:5432/movie_blog"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

app.config["SECRET_KEY"] = "1385"

login_manager = LoginManager(app)
login_manager.login_view = "login"


# database tables
class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(100))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.now)
    review = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"movie : {self.title}  id : {self.id} "


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    movies = db.relationship("Movie", backref="author", lazy=True)


# flask routes
@app.route("/")
def index():
    return redirect(url_for("login_page"))


@app.route("/home")
def home():
    movies = Movie.query.all()
    return render_template("home.html", movies=movies)


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

    user_id = current_user.id

    new_movie = Movie(
        title=title,
        director=director,
        year=year,
        rating=rating,
        review=review,
        user_id=user_id,
    )

    db.session.add(new_movie)
    db.session.commit()

    return redirect(url_for("home"))


@app.route("/delete/<int:id>", methods=["POST"])
def delete_blog(id):
    movie = Movie.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()

    return redirect(url_for("home"))


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

    return redirect(url_for("home"))


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


@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("login_page"))


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("wrong password or username")

    return redirect(url_for("login_page"))


@app.route("/login_page")
def login_page():
    return render_template("login.html")


@app.route("/register_page")
def register_page():
    return render_template("register.html")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/my_reviews")
@login_required
def my_reviews():
    movies = Movie.query.filter_by(user_id=current_user.id).all()
    return render_template("my_reviews.html", movies=movies)


if __name__ == "__main__":
    app.run(debug=True)
