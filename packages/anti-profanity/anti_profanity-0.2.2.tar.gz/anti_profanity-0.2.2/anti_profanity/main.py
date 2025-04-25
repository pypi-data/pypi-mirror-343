from .data import BengaliProfanity, EnglishProfanity, HindiProfanity
import re
import inspect


class ProfanityFilter:
    def __init__(self, lang=None):
        """
        Initialize a profanity filter for one or multiple languages.

        :param lang: String or list of language codes ("en", "hi", "bn")
                    If None, English ("en") will be used by default.
        """
        self.supported_languages = {
            "en": EnglishProfanity,
            "hi": HindiProfanity,
            "bn": BengaliProfanity
        }

        self.profanity_lists = {}

        if lang is None:
            self.profanity_lists["en"] = self.supported_languages["en"]
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
        

    def censor_profanity(self, text, replacement="*", lang=None, case_sensitive=False, semi=False):
        """
        Censor profanity in the given text.
        
        :param text: The input text to be censored.
        :param replacement: The character to replace profanity with. Default is "*".
                           Each character in the profane word will be replaced with this character.
        :param lang: Optional language filter to apply. If None, use all initialized languages.
        :param case_sensitive: If True, performs case-sensitive matching. Default is False.
        :param semi: If True, only the first letter of the profane word will be visible, rest will be censored.
        :return: The censored text.
        """
        languages_to_check = self._get_languages_to_check(lang)
        
        for language in languages_to_check:
            profanity_list = self.profanity_lists.get(language, [])
            
            for word in profanity_list:
                if case_sensitive:
                    pattern = r'\b' + re.escape(word) + r'\b'
                    flags = 0
                else:
                    pattern = r'\b' + re.escape(word) + r'\b'
                    flags = re.IGNORECASE

                def repl(m):
                    w = m.group(0)
                    if semi and len(w) > 1:
                        return w[0] + (replacement * (len(w) - 1))
                    elif semi and len(w) == 1:
                        return w
                    else:
                        return replacement * len(w)

                text = re.sub(pattern, repl, text, flags=flags)
                    
        return text
    
    def is_profanity(self, text, lang=None, case_sensitive=False):
        """
        Check if the text contains profanity.
        
        :param text: The input text to be checked.
        :param lang: Optional language filter to apply. If None, use all initialized languages.
        :param case_sensitive: If True, performs case-sensitive matching. Default is False.
        :return: True if profanity is found, False otherwise.
        """
        languages_to_check = self._get_languages_to_check(lang)
        
        for language in languages_to_check:
            profanity_list = self.profanity_lists.get(language, [])
            
            for word in profanity_list:
                if case_sensitive:
                    pattern = r'\b' + re.escape(word) + r'\b'
                    if re.search(pattern, text):
                        return True
                else:
                    pattern = r'\b' + re.escape(word) + r'\b'
                    if re.search(pattern, text, re.IGNORECASE):
                        return True
                    
        return False
    
    def remove_profanity(self, text, lang=None, case_sensitive=False):
        """
        Remove profanity from the given text.
        
        :param text: The input text to be cleaned.
        :param lang: Optional language filter to apply. If None, use all initialized languages.
        :param case_sensitive: If True, performs case-sensitive matching. Default is False.
        :return: The cleaned text without profanity.
        """
        languages_to_check = self._get_languages_to_check(lang)
        
        for language in languages_to_check:
            profanity_list = self.profanity_lists.get(language, [])
            
            for word in profanity_list:
                if case_sensitive:
                    pattern = r'\b' + re.escape(word) + r'\b'
                    text = re.sub(pattern, "", text)
                else:
                    pattern = r'\b' + re.escape(word) + r'\b'
                    text = re.sub(pattern, "", text, flags=re.IGNORECASE)
                
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
        
    def list_languages(self):
        """
        List all available language codes supported by the profanity filter.

        :return: List of supported language codes.
        """
        return list(self.supported_languages.keys())
    
    def list_methods(self):
        """
        List all available public methods of the ProfanityFilter class along with their arguments.
        
        :return: Dictionary containing method names as keys and their parameters as values.
        """
        methods = {}
        for attr_name in dir(self):
            if attr_name.startswith('_'):
                continue
                
            attr = getattr(self, attr_name)
            if callable(attr):
                signature = inspect.signature(attr)
                params = []
                for param_name, param in signature.parameters.items():
                    if param_name == 'self':
                        continue
                    
                    if param.default == inspect.Parameter.empty:
                        params.append(param_name)
                    else:
                        default_val = param.default
                        if isinstance(default_val, str):
                            default_val = f'"{default_val}"'
                        params.append(f"{param_name}={default_val}")
                
                methods[attr_name] = {
                    'params': params,
                    'doc': inspect.getdoc(attr)
                }
        
        return methods