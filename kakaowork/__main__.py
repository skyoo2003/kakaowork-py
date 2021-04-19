import sys


def main():
    try:
        from kakaowork.command import cli, CLIOptions
        cli(obj=CLIOptions())
    except ImportError:
        sys.exit('Does not support CLI')


if __name__ == '__main__':
    main()
