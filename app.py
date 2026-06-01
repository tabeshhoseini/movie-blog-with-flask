from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
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
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

database_url = os.environ.get("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


migrate = Migrate(app, db)
bcrypt = Bcrypt(app)


login_manager = LoginManager(app)
login_manager.login_view = "login"


# database structure

likes = db.Table(
    "likes",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("blog_id", db.Integer, db.ForeignKey("blogs.id"), primary_key=True),
)


class Blog(db.Model):
    __tablename__ = "blogs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(100))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.now)
    review = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    likes_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"blog : {self.title}  id : {self.id} "


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    Blogs = db.relationship("Blog", backref="author", lazy=True)
    liked_movies = db.relationship(
        "Blog",
        secondary=likes,
        backref=db.backref("liked_by", lazy="dynamic"),
        lazy="dynamic",
    )


# flask logic
@app.route("/")
def index():
    return redirect(url_for("login_page"))


@app.route("/home")
def home():
    blogs = Blog.query.all()
    liked_ids = {blog.id for blog in current_user.liked_movies}
    return render_template("home.html", movies=blogs, liked_id=liked_ids)


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

    new_blog = Blog(
        title=title,
        director=director,
        year=year,
        rating=rating,
        review=review,
        user_id=user_id,
    )

    db.session.add(new_blog)
    db.session.commit()

    return redirect(url_for("home"))


@app.route("/delete/<int:id>", methods=["POST"])
def delete_blog(id):
    blog = Blog.query.get_or_404(id)
    db.session.delete(blog)
    db.session.commit()

    return redirect(url_for("home"))


@app.route("/edit/<int:id>", methods=["GET"])
def edit_blog(id):
    blog = Blog.query.get_or_404(id)
    return render_template("edit.html", movie=blog)


@app.route("/update/<int:id>", methods=["POST"])
def update_blog(id):
    blog = Blog.query.get_or_404(id)

    blog.title = request.form.get("movie_title")
    blog.director = request.form.get("director")

    try:
        blog.year = int(request.form.get("year", 0) or 0)
    except ValueError:
        blog.year = None

    try:
        blog.rating = float(request.form.get("rating", 0) or 0)
    except ValueError:
        blog.rating = None

    blog.review = request.form.get("review")

    db.session.commit()

    return redirect(url_for("home"))


@app.route("/search")
def search():
    query = request.args.get("query", "")

    if query:
        blogs = Blog.query.filter(
            (Blog.title.contains(query)) | (Blog.director.contains(query))
        ).all()
    else:
        blogs = []

    liked_ids = {blog.id for blog in current_user.liked_movies}

    return render_template(
        "search.html", movies=blogs, query=query, liked_ids=liked_ids
    )


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
    blogs = Blog.query.filter_by(user_id=current_user.id).all()
    liked_ids = {blog.id for blog in current_user.liked_movies}
    return render_template("my_reviews.html", movies=blogs, liked_ids=liked_ids)


@app.route("/like/<int:blog_id>", methods=["POST"])
@login_required
def toggle_like(blog_id):
    blog = Blog.query.get_or_404(blog_id)

    if current_user in blog.liked_by:
        blog.liked_by.remove(current_user)
        blog.likes_count -= 1
        liked = False
    else:
        blog.liked_by.append(current_user)
        blog.likes_count += 1
        liked = True

    db.session.commit()
    return jsonify({"liked": liked, "count": blog.likes_count})


if __name__ == "__main__":
    app.run(debug=True)
