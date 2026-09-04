import math

from agent import Agent


def function(x: float, y: float) -> float:
    return 1 - math.log10(x * x + math.cos(y))


def main():
    agent = Agent(function)
    agent.main()


if __name__ == '__main__':
    main()
