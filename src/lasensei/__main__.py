"""Run from source with PYTHONPATH=src python -m lasensei ..."""
import argparse
import json
from .lab_registry import LABS, RUNNERS
from .chapter_demos import RUNNERS as CHAPTERS


def main():
    parser = argparse.ArgumentParser(description='LA-SENSEI: experiments from One Language, Many Dialects')
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('list', help='List the six extended labs')
    lab = commands.add_parser('lab', help='Run a book-aligned lab')
    lab.add_argument('name', choices=sorted(LABS))
    chapter = commands.add_parser('chapter', help='Run selected computational exercises of a chapter')
    chapter.add_argument('number', type=int, choices=range(1, 15), metavar='{1..14}')
    args = parser.parse_args()
    if args.command == 'list':
        for k, (title, path, book_label) in LABS.items():
            print(f'{k:12} Book Lab {book_label}: {title} ({path})')
    elif args.command == 'lab':
        print(json.dumps(RUNNERS[args.name](), indent=2, ensure_ascii=False))
    else:
        print(json.dumps(CHAPTERS[args.number](), indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
