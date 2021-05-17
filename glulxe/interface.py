#!/usr/bin/env python3

__version__ = '0.0.3'

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


class i7Game:
    def __init__( self, gblorb_file, interactive=True ):
        self.file = gblorb_file
        self.tmpdir = tempfile._get_default_tempdir()
        self.tmpfile = os.path.join( self.tmpdir, next( tempfile._get_candidate_names() ) )
        self.game = None

        if interactive:
            for i in self.run():
                print( i )
        
    def _clean( self, string ):
        stri = string.replace( b'\r', b'\n' )
        stri = newline_re.sub( rb' ', stri )
        stri = extra_re.sub( rb' ', stri )
        stri = extra2_re.sub( rb' ', stri )
        stri = stri.decode()
        stri = ''.join( [ i for i in filter( lambda x: ord( x ) != 15, stri ) ] )
        stri = stri.replace( '\n ', '\n' ).replace( '   ', ' ' ).replace( '  ', '' ).strip()
        return stri

    def filter( self, cmd ):
        '''OVERRIDE THIS TO ADD YOUR FILTER'''
        return cmd

    def run( self ):
        f = open( self.tmpfile, 'wb' )
        f.close()
        game = px.spawn( "/bin/bash -c 'glulxe \"%s\" > %s'" % ( self.file, self.tmpfile ) )
        game.setecho( False )
    
        last = 0
        llast = 0

        while True:

            game.sendline( ' ' )
    
            f = open( self.tmpfile, 'rb' )
            new =  [ x for x in enumerate( f.readlines() ) ][ last: ]
            for n, i in new:
                line = self._clean( i ).split( '\n' )
                previous = ''
                exline = [ i for i in enumerate( line ) ][ llast+1: ]
                for m, l in exline:
                    if 'I beg your pardon?' in l and ( previous in ( '> ', '' ) ):
                        continue
                
                    previous = l
                    if l[ 0 ] == '>':
                        continue
                    yield l 
                    llast = m
            

            f.close()
            cmd = input( '--> ' )

            game.sendline( self.filter( cmd ) )


usage = '''start.py [gblorb file]'''

if __name__ == '__main__':
    if len( sys.argv ) != 2:
        print( usage )
    else:
        iffile = sys.argv[ 1 ]
        #main( iffile )
        i = i7Game( iffile )
