import sys


def main():  # noqa: D103
    try:
        from kakaowork.command import cli
        cli()
    except ImportError as e:
        sys.exit(f'Does not support CLI: ({e})')


if __name__ == '__main__':
    main()
