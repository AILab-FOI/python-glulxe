#!/usr/bin/env python3
import sys
import pexpect as px
from glulxe.interface import i7Game

def filter( cmd ):
    if 'ask' in cmd and 'lady' in cmd and 'cheese' in cmd:
        ex = px.spawn( 'xsb --nobanner --quietload --noprompt cheese_expert' )
        ex.interact()
        return 'i'
    return cmd

def main( gblorb ):
    game = i7Game( gblorb, interactive=False )
    game.filter = filter
    for output in game.run():
        print( output )
    

if __name__ == '__main__':
    main( sys.argv[ 1 ] )

