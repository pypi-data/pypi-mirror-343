from .data import BengaliProfanity, EnglishProfanity, HindiProfanity
import re
import inspect
from functools import lru_cache
from typing import Union, List, Dict, Set, Tuple, Optional, Any


class ProfanityFilter:
    def __init__(self, lang: Optional[Union[str, List[str], Tuple[str, ...]]] = None):
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

        # Compiled regex patterns cache - will be populated on demand
        self._pattern_cache = {}
        
        # Initialize profanity lists
        self.profanity_lists = {}
        self._initialize_languages(lang)

    def _initialize_languages(self, lang: Optional[Union[str, List[str], Tuple[str, ...]]]) -> None:
        """
        Initialize the profanity lists for the specified languages.
        
        :param lang: Language specification (string, list, tuple, or None)
        """
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

    def add_language(self, lang_code: str, profanity_list: List[str]) -> None:
        """
        Add a custom language to the profanity filter.
        
        :param lang_code: The language code to use (e.g., "fr", "es")
        :param profanity_list: List of profane words in the language
        """
        if not isinstance(lang_code, str):
            raise TypeError("Language code must be a string")
        if not isinstance(profanity_list, list):
            raise TypeError("Profanity list must be a list of strings")
            
        self.supported_languages[lang_code] = profanity_list
        self.profanity_lists[lang_code] = profanity_list
        
        # Clear pattern cache when adding a new language
        self._pattern_cache = {}

    @lru_cache(maxsize=128)
    def _get_compiled_pattern(self, word: str, case_sensitive: bool) -> re.Pattern:
        """
        Get or create a compiled regex pattern for a word.
        
        :param word: The word to create a pattern for
        :param case_sensitive: Whether the pattern should be case sensitive
        :return: Compiled regex pattern
        """
        # Use word boundaries for Latin scripts, looser boundaries for others
        has_non_latin = bool(re.search(r'[^\x00-\x7F]', word))
        
        if has_non_latin:
            # For non-Latin scripts, use looser word boundaries
            pattern = r'(?:^|[^\w])' + re.escape(word) + r'(?:$|[^\w])'
        else:
            # For Latin scripts, use standard word boundaries
            pattern = r'\b' + re.escape(word) + r'\b'
            
        flags = 0 if case_sensitive else re.IGNORECASE
        return re.compile(pattern, flags)

    def _get_languages_to_check(self, lang: Optional[Union[str, List[str], Tuple[str, ...]]]) -> List[str]:
        """
        Helper method to determine which languages to check based on input.
        
        :param lang: Language specification (string, list, tuple, or None)
        :return: List of language codes to check
        """
        if lang is None:
            return list(self.profanity_lists.keys())
        elif isinstance(lang, str):
            if lang not in self.supported_languages:
                raise ValueError(f"Unsupported language: {lang}")
            return [lang]
        elif isinstance(lang, (list, tuple)):
            unsupported = [l for l in lang if l not in self.supported_languages]
            if unsupported:
                raise ValueError(f"Unsupported language(s): {', '.join(unsupported)}")
            return list(lang)
        else:
            raise TypeError("Language must be a string, list, tuple, or None")

    def censor_profanity(self, text: str, replacement: str = "*", 
                        lang: Optional[Union[str, List[str], Tuple[str, ...]]] = None, 
                        case_sensitive: bool = False, semi: bool = False) -> str:
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
        if not isinstance(text, str):
            raise TypeError("Input text must be a string")
            
        if not text:
            return text
            
        languages_to_check = self._get_languages_to_check(lang)
        result = text
        
        for language in languages_to_check:
            profanity_list = self.profanity_lists.get(language, [])
            
            for word in profanity_list:
                pattern = self._get_compiled_pattern(word, case_sensitive)

                def repl(m):
                    w = m.group(0)
                    # Preserve leading/trailing non-word chars
                    lead, core, trail = '', w, ''
                    if not w.isalnum():
                        # Find the actual word within the matched text
                        word_match = re.search(r'[^\W_]+', w)
                        if word_match:
                            start, end = word_match.span()
                            lead = w[:start]
                            core = w[start:end]
                            trail = w[end:]
                    
                    if semi and len(core) > 1:
                        return lead + core[0] + (replacement * (len(core) - 1)) + trail
                    elif semi and len(core) <= 1:
                        return w
                    else:
                        return lead + (replacement * len(core)) + trail

                result = pattern.sub(repl, result)
                    
        return result
    
    def is_profanity(self, text: str, 
                     lang: Optional[Union[str, List[str], Tuple[str, ...]]] = None, 
                     case_sensitive: bool = False) -> bool:
        """
        Check if the text contains profanity.
        
        :param text: The input text to be checked.
        :param lang: Optional language filter to apply. If None, use all initialized languages.
        :param case_sensitive: If True, performs case-sensitive matching. Default is False.
        :return: True if profanity is found, False otherwise.
        """
        if not isinstance(text, str):
            raise TypeError("Input text must be a string")
            
        if not text:
            return False
            
        languages_to_check = self._get_languages_to_check(lang)
        
        for language in languages_to_check:
            profanity_list = self.profanity_lists.get(language, [])
            
            for word in profanity_list:
                pattern = self._get_compiled_pattern(word, case_sensitive)
                if pattern.search(text):
                    return True
                    
        return False
    
    def remove_profanity(self, text: str, 
                         lang: Optional[Union[str, List[str], Tuple[str, ...]]] = None, 
                         case_sensitive: bool = False) -> str:
        """
        Remove profanity from the given text.
        
        :param text: The input text to be cleaned.
        :param lang: Optional language filter to apply. If None, use all initialized languages.
        :param case_sensitive: If True, performs case-sensitive matching. Default is False.
        :return: The cleaned text without profanity.
        """
        if not isinstance(text, str):
            raise TypeError("Input text must be a string")
            
        if not text:
            return text
            
        languages_to_check = self._get_languages_to_check(lang)
        result = text
        
        for language in languages_to_check:
            profanity_list = self.profanity_lists.get(language, [])
            
            for word in profanity_list:
                pattern = self._get_compiled_pattern(word, case_sensitive)
                result = pattern.sub("", result)
                
        return result
    
    def list_languages(self) -> List[str]:
        """
        List all available language codes supported by the profanity filter.

        :return: List of supported language codes.
        """
        return list(self.supported_languages.keys())
    
    def list_methods(self) -> Dict[str, Dict[str, Any]]:
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