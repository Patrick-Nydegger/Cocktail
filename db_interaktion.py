"""
This file handles database interaction.
"""

from sqlalchemy import create_engine, MetaData, Table, select, func

# Establish a connection to the SQLite database
engine = create_engine('sqlite:///Recipes.db')
metadata = MetaData()

# Load tables
Recipe = Table('Recipe', metadata, autoload_with=engine)
Ingredients = Table('Ingredients', metadata, autoload_with=engine)
recipe_ingredients = Table('recipe_ingredients', metadata, autoload_with=engine)


# Search for recipes that can be made with a list of available ingredients.
# Sorted by the frequency of the ingredients used.
def find_recipes_with_ingredients(available_ingredients):
    with engine.connect() as conn:
        # Subquery: Search for IDs of ingredients that are in the available list
        subquery = (
            select(recipe_ingredients.c.Reciperecipe_ID)
            .join(Ingredients, recipe_ingredients.c.Ingredientsingredients_ID == Ingredients.c.ingredients_ID)
            .where(Ingredients.c.ingredient_name.in_(available_ingredients))
            .group_by(recipe_ingredients.c.Reciperecipe_ID)
            .with_only_columns(
                recipe_ingredients.c.Reciperecipe_ID,
                func.count(recipe_ingredients.c.Ingredientsingredients_ID).label('ingredient_count')
            )
        ).subquery()

        # Main query: Combine recipes with the subquery and sort by ingredient_count
        query = (
            select(Recipe.c.recipe_ID, Recipe.c.name, Recipe.c.method, subquery.c.ingredient_count)
            .join(subquery, Recipe.c.recipe_ID == subquery.c.Reciperecipe_ID)
            .order_by(subquery.c.ingredient_count.desc())
        )

        # Fetch the results of the main query
        main_results = conn.execute(query).fetchall()

        # Fetch the ingredient list with quantities for each recipe
        recipes = []
        for row in main_results:
            ingredients_query = (
                select(
                    Ingredients.c.ingredient_name,
                    recipe_ingredients.c.amount,
                    recipe_ingredients.c.unit_of_measurement
                )
                .join(recipe_ingredients,
                      Ingredients.c.ingredients_ID == recipe_ingredients.c.Ingredientsingredients_ID)
                .where(recipe_ingredients.c.Reciperecipe_ID == row.recipe_ID)
            )

            ingredients = [
                f"{ingredient_row.amount} {ingredient_row.unit_of_measurement or ''} {ingredient_row.ingredient_name}"
                .strip()

                for ingredient_row in conn.execute(ingredients_query).fetchall()
            ]

            # Compile recipe data
            recipes.append({
                'name': row.name,
                'method': row.method,
                'ingredient_count': row.ingredient_count,
                'ingredients': ingredients
            })

    return recipes
