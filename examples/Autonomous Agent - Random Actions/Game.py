from constants import (
    AGENT1_USERNAME,
    AGENT1_PASSWORD,
    AGENT1_SHOW_MESSAGES,
    AGENT2_USERNAME,
)
from utils import (
    generate_server_connection,
    stop_agent,
    generate_message,
)

from spade import agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour, OneShotBehaviour

from time import sleep
import asyncio
import pexpect as px
import re
import sys
import os
import tempfile


GAME_FILE_NAME = "castle.gblorb"
EXIT_COMMANDS = ["quit", "exit"]
BLACKLISTED_COMMANDS = ["disarm", "teleport"]
MAX_SEC_ACTION_WAIT = 60

asc_re = re.compile(r"\\x[0-9a-h\)\[;rml\?HJM]+")
tmpdir = tempfile._get_default_tempdir()
tmpfile = os.path.join(tmpdir, next(tempfile._get_candidate_names()))

game = None
last = 0
llast = 0


def teleport_action():
    game.sendline("teleport")
    print_game_response()
    pass


def disarm_action():
    game.sendline("disarm")
    print_game_response()
    pass


ACTIONS = {
    "TELEPORT": teleport_action,
    "DISARM": disarm_action,
}


def process_npc_action(action):
    action = ACTIONS[action]
    if action is None:
        return

    action()


def print_message(message):
    if AGENT1_SHOW_MESSAGES:
        print(message)


class GameInterrupterAgent(agent.Agent):
    class ActionsBehav(CyclicBehaviour):
        async def run(self):
            message = await self.receive(timeout=MAX_SEC_ACTION_WAIT)

            if message:
                action = message.body
                print_message(f"Action from NPC: {action}")
                process_npc_action(action)

    async def setup(self):
        print_message("Agent is starting...")

        actions_behaviour = self.ActionsBehav()
        self.add_behaviour(actions_behaviour)


def start_agent():
    connection = generate_server_connection(AGENT1_USERNAME, AGENT1_PASSWORD)
    agent = GameInterrupterAgent(*connection)
    agent.start()

    return agent


async def process_command(command, agent):
    # is exit command?
    if command in EXIT_COMMANDS:
        return True

    # is disallowed command?
    if command in BLACKLISTED_COMMANDS:
        print("That's not a verb I recognise.")

        return False

    # process valid commands
    game.sendline(command)

    return False


def clean(string):
    string = string.replace(r"\r", r"\n")
    string = asc_re.sub(r"", string)
    return eval(string).decode()


def print_game_response():
    global game, last, llast

    game.sendline(" ")
    f = open(tmpfile, "rb")
    new = [x for x in enumerate(f.readlines())][last:]
    for n, i in new:
        line = clean(str(i)).split("\n")
        previous = ""
        exline = [i for i in enumerate(line)][llast + 1 :]
        for m, l in exline:
            if "I beg your pardon?" in l and previous == "> ":
                continue
            previous = l
            if l[0] == ">":
                continue
            print(l)
            llast = m
    f.close()
    f.close()

    print("\n")


def start_game(file_name):
    file = open(tmpfile, "wb")
    file.close()

    global game
    game = px.spawn("/bin/bash -c 'glulxe \"%s\" > %s'" % (file_name, tmpfile))
    game.setecho(False)


async def main():
    agent = start_agent()
    start_game(GAME_FILE_NAME)

    while True:
        print_game_response()
        cmd = input()

        should_exit = await process_command(cmd.lower(), agent)

        if should_exit:
            break

    stop_agent(agent)


if __name__ == "__main__":
    asyncio.run(main())
