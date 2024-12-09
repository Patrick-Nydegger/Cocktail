from sqlalchemy import create_engine, MetaData, Table, select, func
import textwrap

# Verbindung zur SQLite-Datenbank herstellen
engine = create_engine('sqlite:///Recipes.db')
metadata = MetaData()

# Tabellen laden
Recipe = Table('Recipe', metadata, autoload_with=engine)
Ingredients = Table('Ingredients', metadata, autoload_with=engine)
recipe_ingredients = Table('recipe_ingredients', metadata, autoload_with=engine)

#def format_amount(amount):
    #"""
    #Formatiert den Mengenwert, um ihn leserlich und wie in einem Rezeptbuch darzustellen.
    #"""
    # Rundet Werte mit Nachkommastellen (z. B. 1.500 auf 1.5) oder gibt ganze Zahlen direkt aus
    #return int(amount) if amount == int(amount) else round(amount, 1)

def find_recipes_with_ingredients(available_ingredients):
    """
    Sucht Rezepte, die mit einer Liste vorhandener Zutaten gemacht werden können.
    Sortiert nach der Häufigkeit der verwendeten Zutaten.
    """
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

# Rezepte suchen
#recipes = find_recipes_with_ingredients(normalized_classes)

"""
print("Gefundene Rezepte:")
#for recipe in recipes:
    #print(f"{recipe['name']} \n - Zutaten: {', '.join(recipe['ingredients'])} \n - Methode: {recipe['method']} \n {150*'='}")


for recipe in recipes:
    print(f"{recipe['name']}\nZutaten:")
    for ingredient in recipe['ingredients']:
        print(f"   {ingredient}")

    # Methode formatieren und umbrechen
    wrapped_method = textwrap.fill(recipe['method'], width=80)
    print(f"Methode:\n{wrapped_method}\n{'=' * 80}")
"""