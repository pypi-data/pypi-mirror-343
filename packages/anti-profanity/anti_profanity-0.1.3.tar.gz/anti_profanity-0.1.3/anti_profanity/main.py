from .data.bn_profanity import bn_profanity
from .data.en_profanity import en_profanity
from .data.hi_profanity import hi_profanity


class ProfanityFilter:
    def __init__(self, lang=None):
        """
        Initialize a profanity filter for one or multiple languages.
        
        :param lang: String or list of language codes ("en", "hi", "bn")
                    If None, all supported languages will be used.
        """
        self.supported_languages = {
            "en": en_profanity,
            "hi": hi_profanity,
            "bn": bn_profanity
        }
        
        self.profanity_lists = {}
        
        if lang is None:
            self.profanity_lists = self.supported_languages
        elif isinstance(lang, str):
            if lang not in self.supported_languages:
                raise ValueError(f"Unsupported language: {lang}")
            self.profanity_lists[lang] = self.supported_languages[lang]
        elif isinstance(lang, (list, tuple)):
            for language in lang:
                if language not in self.supported_languages:
                    raise ValueError(f"Unsupported language: {language}")
                self.profanity_lists[language] = self.supported_languages[language]
        else:
            raise TypeError("Language must be a string, list, tuple, or None")
    
    def censor_profanity(self, text, replacement="*", lang=None):
        """
        Censor profanity in the given text.
        
        :param text: The input text to be censored.
        :param replacement: The character to replace profanity with. Default is "*".
                           Each character in the profane word will be replaced with this character.
        :param lang: Optional language filter to apply. If None, use all initialized languages.
        :return: The censored text.
        """
        languages_to_check = self._get_languages_to_check(lang)
        
        for language in languages_to_check:
            profanity_list = self.profanity_lists.get(language, [])
            
            for word in profanity_list:
                text = text.replace(word, replacement * len(word))
                    
        return text
    
    def is_profanity(self, text, lang=None):
        """
        Check if the text contains profanity.
        
        :param text: The input text to be checked.
        :param lang: Optional language filter to apply. If None, use all initialized languages.
        :return: True if profanity is found, False otherwise.
        """
        languages_to_check = self._get_languages_to_check(lang)
        
        for language in languages_to_check:
            profanity_list = self.profanity_lists.get(language, [])
            
            for word in profanity_list:
                if word in text:
                    return True
                    
        return False
    
    def remove_profanity(self, text, lang=None):
        """
        Remove profanity from the given text.
        
        :param text: The input text to be cleaned.
        :param lang: Optional language filter to apply. If None, use all initialized languages.
        :return: The cleaned text without profanity.
        """
        languages_to_check = self._get_languages_to_check(lang)
        
        for language in languages_to_check:
            profanity_list = self.profanity_lists.get(language, [])
            
            for word in profanity_list:
                text = text.replace(word, "")
                
        return text
    
    def _get_languages_to_check(self, lang):
        """
        Helper method to determine which languages to check based on input.
        
        :param lang: Language specification (string, list, or None)
        :return: List of language codes to check
        """
        if lang is None:
            return self.profanity_lists.keys()
        elif isinstance(lang, str):
            if lang not in self.supported_languages:
                raise ValueError(f"Unsupported language: {lang}")
            return [lang]
        elif isinstance(lang, (list, tuple)):
            for language in lang:
                if language not in self.supported_languages:
                    raise ValueError(f"Unsupported language: {language}")
            return lang
        else:
            raise TypeError("Language must be a string, list, tuple, or None")


# Usage examples:
# # Initialize with one language
# filter_en = ProfanityFilter("en")
# 
# # Initialize with multiple languages
# filter_multi = ProfanityFilter(["en", "hi"])
# 
# # Initialize with all languages
# filter_all = ProfanityFilter()
# 
# # Censor text with default replacement
# censored = filter_multi.censor_profanity("Some text with bad words")
# 
# # Censor text with custom replacement character
# censored = filter_multi.censor_profanity("Some text with bad words", replacement="#")
# 
# # Censor text with specific language filter
# censored = filter_all.censor_profanity("Some text with bad words", lang="en")