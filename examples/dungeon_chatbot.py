#!/usr/bin/env python3
import sys

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

from glulxe.interface import i7Game

def train( bot ):
    bot.set_trainer( ListTrainer )

    bot.train( [ 'look around', 'look' ] )
    bot.train( [ 'where am i', 'look' ] )
    bot.train( [ 'what is this place', 'look' ] )
    bot.train( [ 'give me that torch', 'take torch' ] )
    bot.train( [ 'i want that torch', 'take torch' ] )
    bot.train( [ 'take that torch', 'take torch' ] )
    bot.train( [ 'what is in that chest', 'open chest' ] )
    bot.train( [ 'let me open that chest', 'open chest' ] )
    bot.train( [ 'yay chese', 'take cheese' ] )
    bot.train( [ 'i want the cheese', 'take cheese' ] )
    bot.train( [ 'i will make a cheesburger', 'take cheese' ] )
    bot.train( [ 'take the cheddar', 'take cheese' ] )
    bot.train( [ 'take the gorgonzola', 'take cheese' ] )
   

def main( gblorb ):
    bot = ChatBot( 'DUNGEON_KEEPER', read_only=False, database_uri='sqlite:///DUNGEON.sqlite3' )
    train( bot )
    bot = ChatBot( 'DUNGEON_KEEPER', read_only=True, database_uri='sqlite:///DUNGEON.sqlite3' )
    game = i7Game( gblorb, interactive=False )
    game.filter = lambda cmd: str( bot.get_response( cmd ) )
    print( game.filter( 'get the cheddar' ) )
    for output in game.run():
        print( output )
    

if __name__ == '__main__':
    main( sys.argv[ 1 ] )
