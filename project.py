import requests
import json
import os
import re
import time

from dotenv import load_dotenv
load_dotenv()  

API_KEY = os.getenv("API_KEY")
CACHE_DIR = "cache"

def main():
    while True:
        ingredients = get_ingredients()
        ingredients = validate_ingredients(ingredients)
        if ingredients is not None:
            break
        print("Invalid ingredients.")

    while True:
        try:
            num_recipes = recipe_number()
            if 1 <= num_recipes <= 20:
                break
            else:
                print("Please enter a number between 1 and 20.")
        except ValueError:
            print("Please enter a valid number.")

    meals = create_cache(ingredients, num_recipes)

    print("\nRecipe Names:")
    for i, meal in enumerate(meals, 1):
        title = meal.get('title', 'Unknown Name')
        print(f"{i}. {title}")

def get_ingredients():
    return input("What are your ingrdients? ")

def validate_ingredients(ingredients):
    separator_check_regex = r"[,.\~_\"\\ -]"
    split_regex = r"[,.\~_\"\\ -]+"

    if re.search(separator_check_regex, ingredients):
        parts = re.split(split_regex, ingredients)
        cleaned_parts = [part.strip() for part in parts if part.strip()]

        # Remove duplicates
        cleaned_parts = list(set(cleaned_parts))

        for part in cleaned_parts:
            if re.search(r"[@!#$%\*()]", part):
                print(f"Invalid ingredient {part}.")
                return None

        ingredients = ",".join(cleaned_parts)

    return ingredients

def recipe_number():
    return int(input("How many recipe titles do you want? "))

def search_recipes(ingredients, num_recipes, retries=3, delay=2):
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "ingredients": ingredients,
        "number": num_recipes,
        "apiKey": API_KEY
    }
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed (attempt {attempt + 1}/{retries}): {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise

def validate_file_name(ingredients):
    ingredient_order = ingredients.split(",")
    ingredients_ordered = [ingredient.strip() for ingredient in ingredient_order]
    sorted_ingredients = sorted(ingredients_ordered)
    return "_".join(sorted_ingredients)

def create_cache(ingredients, num_recipes):
    os.makedirs(CACHE_DIR, exist_ok=True)
    validated_name = validate_file_name(ingredients)

    cache_filename = os.path.join(CACHE_DIR, f"cache_{validated_name}_{num_recipes}.json")
    prefix = f"cache_{validated_name}_"

    files = os.listdir(CACHE_DIR)
    matching_files = [f for f in files if f.startswith(prefix) and f.endswith(".json")]

    numbers = [int(f[len(prefix):-5]) for f in matching_files]

    try:
        if os.path.exists(cache_filename):
            print(f"Loading from cache: {cache_filename}")
            with open(cache_filename) as file:
                cached_meals = json.load(file)

            max_cached = max(numbers, default=0)
            if max_cached >= num_recipes:
                return cached_meals[:num_recipes]
            else:
                needed = num_recipes - len(cached_meals)
                new_meals = search_recipes(ingredients, needed)
                meals = cached_meals + new_meals
                with open(cache_filename, "w") as file:
                    json.dump(meals, file, indent=4)
                return normalize_meals(meals)

        # no cache yet
        meals = search_recipes(ingredients, num_recipes)
        with open(cache_filename, "w") as file:
            json.dump(meals, file, indent=4)

    except json.JSONDecodeError:
        print("Cache file corrupted. Fetching fresh data.")
        meals = search_recipes(ingredients, num_recipes)
        with open(cache_filename, "w") as file:
            json.dump(meals, file, indent=4)
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return []

    return normalize_meals(meals)

def normalize_meals(meals):
    fixed_meals = []
    if isinstance(meals, list):
        for meal in meals:
            if isinstance(meal, str):
                try:
                    meal = json.loads(meal)
                except json.JSONDecodeError:
                    continue
            if isinstance(meal, dict):
                fixed_meals.append(meal)
    return fixed_meals

if __name__ == "__main__":
    main()
