#!/usr/bin/env python3
import sys
import pexpect as px
import start

def filter( cmd ):
    if 'ask' in cmd and 'lady' in cmd and 'cheese' in cmd:
        ex = px.spawn( 'xsb --nobanner --quietload --noprompt cheese_expert' )
        ex.interact()
        return 'i'
    return cmd

def main( gblorb ):
    start.filter = lambda cmd: filter( cmd )
    start.main( gblorb )
    

if __name__ == '__main__':
    main( sys.argv[ 1 ] )

