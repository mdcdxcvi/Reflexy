import sys


def start():
    """Run the game."""
    from reflexy.runner import Runner

    runner = Runner()
    runner.run()


if __name__ == "__main__":

    start()
    sys.exit()
