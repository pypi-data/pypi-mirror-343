# winiTranslate

**winiTranslate** is a simple Python module that allows you to:
- Translate text
- Detect the language of a text
- List all available languages from Google Translate

## Installation

You can install **winiTranslate** using **pip**:

```bash
pip install winiTranslate
```

If you prefer to install it locally after cloning the repository, use:

```bash
pip install -r requirements.txt
```

## Usage

You can use **winiTranslate** to translate text, detect the language of a text, and list the supported languages by Google Translate.

### Importing the Module

To use the module, simply import the necessary functions like this:

```python
from winiTranslate import translate, detect, list
```

### Example 1: Translate Text

The `translate` function allows you to translate text from one language to another.  
You can specify the source language (or use `'auto'` for automatic detection) and the target language.

```python
from winiTranslate import translate

# Translate text from French to English
text = "Bonjour tout le monde"
translated_text = translate(text, "en")
print(translated_text)  # Output: Hello everyone
```

### Example 2: Detect the Language of a Text

The `detect` function automatically detects the language of the given text.

```python
from winiTranslate import detect

# Detect the language of a text
text = "Bonjour tout le monde"
language_code = detect(text)
print(language_code)  # Output: 'fr' (for French)
```

### Example 3: List All Available Languages

The `list` function returns a dictionary of all languages supported by Google Translate, along with their corresponding language codes.

```python
from winiTranslate import list

# List all available languages
languages = list()
for code, language in languages.items():
    print(f"{code}: {language}")
```

## Functions Available

- `translate(text, target_language, source_language='auto')`
- `detect(text)`
- `list()`

## Example of Language Codes

Here are some examples of supported language codes:

| Code | Language     |
|----- |--------------|
| en   | English      |
| fr   | French       |
| es   | Spanish      |
| de   | German       |
| zh-CN| Chinese (Simplified) |

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
