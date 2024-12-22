from sqlalchemy import create_engine, MetaData, Table, select, func
import textwrap

# Verbindung zur SQLite-Datenbank herstellen
engine = create_engine('sqlite:///Recipes.db')
metadata = MetaData()

# Tabellen laden
Recipe = Table('Recipe', metadata, autoload_with=engine)
Ingredients = Table('Ingredients', metadata, autoload_with=engine)
recipe_ingredients = Table('recipe_ingredients', metadata, autoload_with=engine)

def find_recipes_with_ingredients(available_ingredients):

    #Sucht Rezepte, die mit einer Liste vorhandener Zutaten gemacht werden können.
    #Sortiert nach der Häufigkeit der verwendeten Zutaten.

    with engine.connect() as conn:
        # Unterabfrage: Suche nach IDs der Zutaten, die in der verfügbaren Liste enthalten sind
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

        # Hauptabfrage: Kombiniere Rezepte mit der Unterabfrage und sortiere nach ingredient_count
        query = (
            select(Recipe.c.recipe_ID, Recipe.c.name, Recipe.c.method, subquery.c.ingredient_count)
            .join(subquery, Recipe.c.recipe_ID == subquery.c.Reciperecipe_ID)
            .order_by(subquery.c.ingredient_count.desc())
        )

        # Ergebnisse der Hauptabfrage abrufen
        main_results = conn.execute(query).fetchall()

        # Für jedes Rezept die vollständige Zutatenliste mit Mengenangabe abrufen
        recipes = []
        for row in main_results:
            ingredients_query = (
                select(
                    Ingredients.c.ingredient_name,
                    recipe_ingredients.c.amount,
                    recipe_ingredients.c.unit_of_measurement
                )
                .join(recipe_ingredients, Ingredients.c.ingredients_ID == recipe_ingredients.c.Ingredientsingredients_ID)
                .where(recipe_ingredients.c.Reciperecipe_ID == row.recipe_ID)
            )
            # Zutaten zusammen mit Menge und Einheit abrufen
            ingredients = [
                f"{ingredient_row.amount} {ingredient_row.unit_of_measurement or ''} {ingredient_row.ingredient_name}".strip()
                #f"{format_amount(ingredient_row.amount)} {ingredient_row.unit_of_measurement or ''} {ingredient_row.ingredient_name}".strip()
                for ingredient_row in conn.execute(ingredients_query).fetchall()
            ]

            # Rezeptdaten zusammenstellen
            recipes.append({
                'name': row.name,
                'method': row.method,
                'ingredient_count': row.ingredient_count,
                'ingredients': ingredients
            })

    return recipes


# Beispiel für eine Zutatenliste
#available_ingredients = ["gin","cointrau","champagne","prosecco", "Orange Juice", "Lime"]

