from flask import Flask, request
from flask_restx import Api, Resource, fields
from config import DevConfig
from models import Recipe
from extensions import db
from models import Recipe

app = Flask(__name__)
app.config.from_object(DevConfig)

db.init_app(app)


api = Api(app, doc='/docs')

"""
from flask import Blueprint
from backend.models import Recipe

# Create a Flask-RESTx Blueprint
blueprint = Blueprint('api', __name__, url_prefix='/api')

# Initialize the Flask-RESTx Api with the Blueprint
api = Api(blueprint, doc='/docs')

# Register the Blueprint with the Flask App
app.register_blueprint(blueprint)

"""

#model (serializer)
recipe_model=api.model('Recipe',{
    'id': fields.Integer(),
    'title': fields.String(),
    'description': fields.String()
})



@api.route('/hello')
class HelloResource(Resource):
    def get(self):
        return {'message': 'Hello World'}
    

    
@api.route('/recipes')
class RecipeResource(Resource):
    
    @api.marshal_list_with(recipe_model)
    def get(self):
        #get all recipes
        
        recipes=Recipe.query.all()
        
        return recipes
    
    @api.marshal_with(recipe_model)
    def post(self):
        #create new recipek
        
        data=request.get_json()
        
        new_recipe=Recipe(
            title=data.get('title'),
            description=data.get('description')
        )
        
        new_recipe.save()
        
        return new_recipe,201



@api.route('/recipes/<int:id>')
class RecipeResource(Resource):
    
    @api.marshal_with(recipe_model)
    def get(self,id):
        #get a recipe by id
        
        recipe=Recipe.query.get_or_404(id)
        
        return recipe
        
    @api.marshal_with(recipe_model)
    def put(self,id):
        #update a recipe by id
        
        recipe_to_update=Recipe.query.get_or_404(id)
        
        data=request.get_json()
        
        recipe_to_update.update(data.get('title'),data.get('description'))
        
        return recipe_to_update
    
    @api.marshal_with(recipe_model)
    def delete(self,id):
        #delete a recipe by id
        
        recipe_to_delete=Recipe.query.get_or_404(id)
        
        recipe_to_delete.delete()
        
        return recipe_to_delete
 
"""

@api.route('/recipes')
class RecipeResource(Resource):
    
    @api.marshal_list_with(recipe_model)
    @api.doc(description="Get all recipes")
    def get(self):
        # get all recipes
        recipes = Recipe.query.all()
        return recipes

    @api.doc(description="Create a new recipe")
    def post(self):
        # create new recipe
        pass

    @api.doc(description="Update a recipe by ID")
    def put(self, id):
        # update a recipe by ID
        pass

    @api.doc(description="Delete a recipe by ID")
    def delete(self, id):
        # delete a recipe by ID
        pass

"""
    
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Recipe': Recipe}



if __name__ == '__main__':
    app.run()
