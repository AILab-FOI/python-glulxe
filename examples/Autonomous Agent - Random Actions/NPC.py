from constants import (
    AGENT2_USERNAME,
    AGENT2_PASSWORD,
    AGENT2_SHOW_MESSAGES,
    AGENT1_USERNAME,
)
from utils import (
    generate_server_connection,
    stop_agent,
    generate_message,
)

from spade import agent
from spade.behaviour import PeriodicBehaviour, CyclicBehaviour
from spade.template import Template

from random import randrange, choice
import datetime

MIN_PERIOD_TIME = 20
MAX_PERIOD_TIME = 30
ACTIONS = ["TELEPORT", "DISARM"]


def print_message(message):
    if AGENT2_SHOW_MESSAGES:
        print(message)


def generate_random_period():
    return randrange(MIN_PERIOD_TIME, MAX_PERIOD_TIME)


def generate_action():
    return choice(ACTIONS)


class GameActionsAgent(agent.Agent):
    class RandomActionsBehav(PeriodicBehaviour):
        async def run(self):
            action = generate_action()
            print_message(f"Agent is dispatching {action} action...")
            message = generate_message(AGENT1_USERNAME, action)
            await self.send(message)

            self.period = generate_random_period()

    async def setup(self):
        print_message("Agent is starting...")

        period = generate_random_period()
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=period)
        random_actions_behaviour = self.RandomActionsBehav(
            period=period, start_at=start_at
        )
        self.add_behaviour(random_actions_behaviour)


def start_agent():
    connection = generate_server_connection(AGENT2_USERNAME, AGENT2_PASSWORD)
    agent = GameActionsAgent(*connection)
    agent.start()

    return agent


def main():
    agent = start_agent()
    input("Press ENTER to exit.\n\n")
    stop_agent(agent)


if __name__ == "__main__":
    main()