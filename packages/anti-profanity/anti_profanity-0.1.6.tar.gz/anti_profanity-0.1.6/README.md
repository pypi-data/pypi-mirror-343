# ProfanityFilter

A simple and customizable profanity filtering class supporting multiple languages: English (`en`), Hindi (`hi`), and Bengali (`bn`). It allows you to **censor**, **detect**, or **remove** profane words from a given text.

## Features

- 🔍 Detect profanity in text  
- ✂️ Remove profanity completely  
- ✳️ Censor profanity with a customizable replacement character  
- 🌐 Multilingual support (English, Hindi, Bengali)  
- 💡 Easy to integrate and extend  

---

## Installation

Make sure your profanity word lists are properly structured and located in the appropriate `data` subdirectory:

project/
 ├── Anti-Profanity/
 │ ├── init.py
 │ ├── main.py
 │ └── data /
 │   ├── en_profanity.py 
 │   ├── hi_profanity.py  
 │   └── bn_profanity.py
 ├── readme.md
 └── setup.py

Each language file (e.g., `en_profanity.py`) should export a list of profane words:

```python
from anti-profanity import ProfanityFilter

# For English only
pf_en = ProfanityFilter("en")

# For English and Hindi
pf_multi = ProfanityFilter(["en", "hi"])

# For all supported languages
pf_all = ProfanityFilter()
```
## Methods

### Example 1
```bash
censor_profanity(text, replacement="*", lang=None)
```
Replaces each character of any detected profanity with the replacement character.

```python
text = "This contains badword1."
censored = pf_en.censor_profanity(text)
print(censored)  # Output: This contains ********
```
### Example 2
```bash
is_profanity(text, lang=None)
```
Checks whether the given text contains any profane words.
```
is_dirty = pf_multi.is_profanity("Text with badword2")
print(is_dirty)  # Output: True
```
### Example 3
```
remove_profanity(text, lang=None)
```
Removes all profane words from the given text.
```python
cleaned = pf_en.remove_profanity("Some badword1 text")
print(cleaned)  # Output: Some  text
```

## Customization
You can extend the filter by adding your own languages or editing the existing profanity lists in the `data` directory.


## License

[MIT](https://choosealicense.com/licenses/mit/)

