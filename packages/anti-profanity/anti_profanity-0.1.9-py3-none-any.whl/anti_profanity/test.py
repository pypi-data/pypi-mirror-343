#from anti_profanity import ProfanityFilter

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