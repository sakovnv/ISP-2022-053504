from src.utility.cli import CommandLineInterface


def main():
    cli = CommandLineInterface()
    cli.args_init()
    cli.execution()


if __name__ == "__main__":
    main()
