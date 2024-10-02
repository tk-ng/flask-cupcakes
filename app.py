"""Flask app for Cupcakes"""
from flask import Flask, render_template, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)


@app.route("/")
def index_page():
    return render_template("index.html")


@app.route("/api/cupcakes")
def get_cupcakes():
    cupcakes = Cupcake.query.all()
    data = [c.serialize() for c in cupcakes]
    return jsonify(cupcakes=data)


@app.route("/api/cupcakes/<int:id>")
def get_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    data = cupcake.serialize()
    return jsonify(cupcake=data)


@app.route("/api/cupcakes", methods=["POST"])
def create_cupcakes():
    flavor = request.json['flavor']
    size = request.json['size']
    rating = float(request.json['rating'])
    image = request.json.get('image', None)
    new_cupcake = Cupcake(flavor=flavor, size=size,
                          rating=rating, image=image)
    db.session.add(new_cupcake)
    db.session.commit()
    response = jsonify(cupcake=new_cupcake.serialize())
    return (response, 201)


@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def update_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.image = request.json.get("image", cupcake.image)
    db.session.commit()
    data = cupcake.serialize()
    return jsonify(cupcake=data)


@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def delete_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")
