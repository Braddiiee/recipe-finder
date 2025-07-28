# Recipe Finder

#### Video Demo: <https://youtu.be/xe93YJPWlVg>

#### Description:

**Recipe Finder** is a command-line Python application that allows users to discover recipe titles based on the ingredients they have on hand. Leveraging the Spoonacular recipe API, this project demonstrates concepts in user input validation, file-based caching, API integration, and automated testing.

---

## Features

1. **Ingredient Input and Validation**:
   Users enter a comma-separated (or space-separated) list of ingredients. The program uses regular expressions to remove extra separators, trim whitespace, deduplicate entries, and reject invalid characters (e.g., punctuation or symbols).

2. **Recipe Quantity Selection**:
   After ingredients are validated, users specify the number of recipe titles they’d like—up to a maximum of 20. Input is converted to an integer and range-checked, with user-friendly error messages guiding any corrections.

3. **API Integration with Retries**:
   When a cache miss occurs, the application fetches recipes from Spoonacular’s API. To make the program robust against transient network or rate-limit issues, API requests are wrapped with retry logic (up to three attempts with delays).

4. **File-Based Caching**:
   To minimize repeated API calls and speed up subsequent runs, search results are cached in JSON files stored under a `cache/` directory. Cache filenames are generated from a normalized, sorted underscore-joined string of ingredients plus the requested recipe count.

   * If an exact cache file exists, it is loaded and sliced to the requested size.
   * If a smaller cache exists, only the missing recipes are fetched and appended, then saved.
   * Corrupted cache files automatically trigger a fresh fetch.

5. **Result Display**:
   The program prints a numbered list of recipe titles (or “Unknown Name” if the response payload is unexpected), offering a quick glance at options the user can pursue on the Spoonacular website.

6. **Automated Testing**:
   Under `test_project.py`, three core functions—`validate_ingredients`, `validate_file_name`, and `normalize_meals`—are each accompanied by `pytest` tests. These tests ensure input cleaning, filename normalization, and JSON parsing logic work correctly across edge cases (duplicates, invalid characters, malformed JSON).

7. **Configuration and Dependencies**:

   * External libraries are listed in `requirements.txt` (`requests` for HTTP calls, `pytest` for testing).
   * Sensitive configuration (the `API_KEY`) is loaded from an environment variable—store it in a local `.env` file and add `.env` to `.gitignore` to keep your key private.

---

## Project Structure

```
project/
├── project.py           # Main application with functions and entry point
├── test_project.py      # Automated pytest test suite for core functions
├── requirements.txt     # External dependencies (requests, pytest)
├── .env                 # Environment variable file (API_KEY=...) 
└── cache/               # JSON cache files for API results
```

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Braddiiee/recipe-finder.git
cd recipe-finder
```

### 2. Set Up a Virtual Environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate     # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Your API Key

Create a `.env` file in the root directory and add your Spoonacular API key:

```env
API_KEY=your_spoonacular_api_key_here
```

(You can refer to `.env.example` for the correct format.)

### 5. Run the App

```bash
python project.py
```

### 6. Run the Tests (optional)

```bash
pytest
```


## Design Choices

* **Separation of Concerns**:
  Functions in `project.py` are top-level and focused: one for input gathering, one for validation, one for API calls, one for caching, and one for data normalization. This modularity simplifies testing and future maintenance.

* **Resilient Fetching**:
  Network reliability is addressed by retry logic with backoff delays, reducing user frustration during API hiccups.

* **Intuitive Caching**:
  Cache hits and misses are logged to the console, giving users feedback on load times and offline behavior. Incremental cache updates prevent redundant data downloads.

* **Robust Validation**:
  Ingredient strings are rigorously sanitized to prevent malformed API queries (e.g., stray punctuation) and to standardize naming for cache filenames.

* **Testing-First Mindset**:
  Core logic functions were developed alongside their tests (pytest). 


## Future Improvements

* Expand testing to cover caching logic and error paths.
* Offer full recipe details (ingredients, instructions) rather than just titles.
* Add interactive menu to let users select a recipe to view or save for later.
* Implement asynchronous API calls for faster batch fetching.
* Package as a CLI tool with `argparse` or `click` for scriptable usage.

---


