#!/usr/bin/env python3

import pexpect as px
import re
import sys
import os
import tempfile

asc_re = re.compile( rb'\\x[0-9a-h\)\[;rml\?HJMKB\(q]+' )
newline_re = re.compile( rb'\x1b[^ \n.>]*(?:d|H|J|M|K|B)' )
extra_re = re.compile( rb'\x1b[^a-zA-Z]*m' )
extra2_re = re.compile( rb'\x08' )

tmpdir = tempfile._get_default_tempdir()
tmpfile = os.path.join( tmpdir, next( tempfile._get_candidate_names() ) )

def clean( string ):
    string = string.replace( b'\r', b'\n' )
    string = newline_re.sub( rb' ', string )
    string = extra_re.sub( rb' ', string )
    string = extra2_re.sub( rb' ', string )
    return string.decode()

def filter( cmd ):
    '''OVERRIDE THIS TO ADD YOUR FILTER'''
    if cmd == 'kuku':
        return 'look'
    return cmd



def main( gblorb ):
    print( 'SMH' )
    print( 0 )
    f = open( tmpfile, 'wb' )
    f.close()
    game = px.spawn( "/bin/bash -c 'glulxe \"%s\" > %s'" % ( gblorb, tmpfile ) )
    game.setecho( False )
    
    last = 0
    llast = 0

    print( 1 )

    while True:

        game.sendline( ' ' )
    
        f = open( tmpfile, 'rb' )
        new =  [ x for x in enumerate( f.readlines() ) ][ last: ]
        for n, i in new:
            line = clean( str( i ) ).split( '\n' )
            previous = ''
            exline = [ i for i in enumerate( line ) ][ llast+1: ]
            for m, l in exline:
                if 'I beg your pardon?' in l and previous == '> ':
                    continue
                
                previous = l
                if l[ 0 ] == '>':
                    continue
                yield l 
                llast = m
            

        f.close()
        cmd = input( '--> ' )

        game.sendline( filter( cmd ) )
    

usage = '''start.py [gblorb file]'''

if __name__ == '__main__':
    if len( sys.argv ) != 2:
        print( usage )
    else:
        iffile = sys.argv[ 1 ]
        main( iffile )
