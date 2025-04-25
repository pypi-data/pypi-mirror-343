# pip3 install anti-profanity

from anti_profanity import ProfanityFilter

def test_single_language():
    pf = ProfanityFilter("en")
    result = pf.censor_profanity("Some text with bad words")
    print("Single language (en):", result)

def test_multiple_languages():
    pf = ProfanityFilter(["en", "hi"])
    result = pf.censor_profanity("Some text with bad words")
    print("Multiple languages (en, hi):", result)

def test_default_language():
    pf = ProfanityFilter()
    result = pf.censor_profanity("Some text with bad words", lang="en")
    print("Default language (en):", result)

def test_custom_replacement():
    pf = ProfanityFilter(["en", "hi"])
    result = pf.censor_profanity("Some text with bad words", replacement="#")
    print("Custom replacement (#):", result)

def main():
    test_single_language()
    test_multiple_languages()
    test_default_language()
    test_custom_replacement()

if __name__ == "__main__":
    main()