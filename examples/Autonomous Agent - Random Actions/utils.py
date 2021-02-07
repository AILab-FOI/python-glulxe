from constants import AGENTS_SERVER

from spade.message import Message
from spade.template import Template
from spade import quit_spade


def generate_user(username):
    return f"{username}@{AGENTS_SERVER}"


def generate_server_connection(username, password):
    user = generate_user(username)

    return (user, password)


def generate_message(username, message):
    user = generate_user(username)

    return Message(to=user, body=message)


def stop_agent(agent):
    agent.stop()
    quit_spade()
