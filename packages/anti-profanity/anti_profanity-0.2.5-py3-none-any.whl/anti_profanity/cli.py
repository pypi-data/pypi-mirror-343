import sys
import argparse
from .main import ProfanityFilter
import logging

logging = logging.basicConfig(level=logging.INFO)


def run():
    """
    Command-line interface for the ProfanityFilter.
    """
    parser = argparse.ArgumentParser(description='Anti-Profanity - Multilingual Profanity Filter')
    parser.add_argument('--action', choices=['censor', 'check', 'remove', 'list_langs', 'list_methods'], 
                        required=True, help='Action to perform')
    parser.add_argument('--text', help='Text to process')
    parser.add_argument('--lang', nargs='+', help='Language(s) to use for filtering')
    parser.add_argument('--replacement', default='*', help='Character to use for censoring')
    parser.add_argument('--case-sensitive', action='store_true', help='Enable case-sensitive matching')
    parser.add_argument('--semi', action='store_true', 
                        help='Show first letter of profane words in censoring mode')
    parser.add_argument('--file', help='Input file path (as alternative to --text)')
    parser.add_argument('--output', help='Output file path (optional)')
    
    args = parser.parse_args()
    
    profanity_filter = ProfanityFilter(args.lang)
    
    input_text = ""
    if args.action in ['censor', 'check', 'remove']:
        if args.text:
            input_text = args.text
        elif args.file:
            try:
                with open(args.file, 'r', encoding='utf-8') as f:
                    input_text = f.read()
            except Exception as e:
                logging.ERROR(f"Error reading file: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            if args.action != 'list_langs' and args.action != 'list_methods':
                print("Error: Either --text or --file must be provided", file=sys.stderr)
                sys.exit(1)
    
    result = None
    if args.action == 'censor':
        result = profanity_filter.censor_profanity(
            input_text, 
            replacement=args.replacement, 
            lang=args.lang, 
            case_sensitive=args.case_sensitive,
            semi=args.semi
        )
    elif args.action == 'check':
        result = profanity_filter.is_profanity(
            input_text, 
            lang=args.lang, 
            case_sensitive=args.case_sensitive
        )
        result = f"Profanity {'found' if result else 'not found'} in the text."
    elif args.action == 'remove':
        result = profanity_filter.remove_profanity(
            input_text, 
            lang=args.lang, 
            case_sensitive=args.case_sensitive
        )
    elif args.action == 'list_langs':
        languages = profanity_filter.list_languages()
        result = "Supported languages:\n" + "\n".join([f"- {lang}" for lang in languages])
    elif args.action == 'list_methods':
        methods = profanity_filter.list_methods()
        result = "Available methods:\n"
        for method_name, details in methods.items():
            params_str = ", ".join(details['params'])
            result += f"\n{method_name}({params_str})\n"
            if details['doc']:
                result += f"  {details['doc'].split('\n')[0]}\n"
    
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(str(result))
        except Exception as e:
            logging.ERROR(f"Error writing to output file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(result)


if __name__ == "__main__":
    run()