"""Flask app for Cupcakes"""
from flask import Flask, request, render_template,jsonify
from flask_debugtoolbar import DebugToolbarExtension 
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret" 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def show_homepage():
    return render_template("homepage.html")


@app.route('/api/cupcakes')
def list_cupcakes():
    """Returns JSON w/ all cupcakes"""
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes = all_cupcakes)
  
@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """Returns JSON data for a single cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake = cupcake.serialize())

@app.route('/api/cupcakes', methods=["POST"]) 
def create_cupcake():
    """Create a cupcake with flavor, size, rating and returns JSON of that created cupcake"""
    new_cupcake = Cupcake(flavor = request.json['flavor'], 
                          size = request.json['size'],
                          rating = request.json['rating']
                          )
    db.session.add(new_cupcake)
    db.session.commit()
   
    return(jsonify(cupcake = new_cupcake.serialize()),201)

@app.route('/api/cupcakes/<int:id>' , methods=["PATCH"])
def update_cupcake(id):
    """Update flavor,size,rating and image of a cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get('flavor' , cupcake.flavor)
    cupcake.size = request.json.get('size' , cupcake.size)
    cupcake.rating = request.json.get('rating' , cupcake.rating)
    cupcake.image = request.json.get('image' , cupcake.image)

    db.session.commit()
    return jsonify(cupcake = cupcake.serialize)

@app.route('/api/cupcakes/<int:id>', methods=["DELETE"]) #
def delete_cupcake(id):#
    """Deletes a particular cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted")


