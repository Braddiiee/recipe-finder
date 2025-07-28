from project import validate_ingredients, validate_file_name, normalize_meals

def test_validate_ingredients_cleaning():
    raw_input = "  cheese,,,chicken  ,cheese, beef "
    expected_output = sorted(["cheese", "chicken", "beef"])
    cleaned = validate_ingredients(raw_input)
    assert cleaned is not None
    assert sorted(cleaned.split(",")) == expected_output

def test_validate_ingredients_invalid_characters():
    bad_input = "cheese,@chicken,beef!"
    cleaned = validate_ingredients(bad_input)
    assert cleaned is None

def test_validate_file_name_sorting_and_formatting():
    ingredients = "beef,cheese,chicken"
    expected = "beef_cheese_chicken"
    assert validate_file_name(ingredients) == expected

def test_normalize_meals_handles_strings_and_dicts():
    meals = [
        '{"title": "Chicken Soup"}',
        {"title": "Beef Stew"},
        'INVALID JSON',
        '{"title": "Cheese Omelette"}'
    ]
    normalized = normalize_meals(meals)
    titles = [meal["title"] for meal in normalized]
    assert titles == ["Chicken Soup", "Beef Stew", "Cheese Omelette"]
