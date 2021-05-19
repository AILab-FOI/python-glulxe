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

class i7Game:
    def __init__( self, gblorb_file, filter=None, interactive=True ):
        self.file = gblorb_file
        self.tmpdir = tempfile._get_default_tempdir()
        self.tmpfile = os.path.join( self.tmpdir, next( tempfile._get_candidate_names() ) )
        self.game = None
    
        self.last = 0
        self.llast = 0
        
        self.init()

        if filter:
            self.filter = filter

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

    def init( self ):
        self.fh = open( self.tmpfile, 'wb' )
        self.fh.close()
        self.game = px.spawn( "/bin/bash -c 'glulxe \"%s\" > %s'" % ( self.file, self.tmpfile ) )
        self.game.setecho( False )

    def intro( self ):
        res = ""
        self.game.sendline( ' ' )
        for result in self.step():
            res += '\n' + result
        return res

    def run( self ):
        while True:
            for result in self.step():
                yield result
            cmd = input( '--> ' )
            self.game.sendline( self.filter( cmd ) )

    def next( self, cmd ):
        res = ""
        self.game.sendline( self.filter( cmd ) )
        for result in self.step():
            res += '\n' + result
        return res

    def step( self ):
        self.game.sendline( ' ' )
    
        self.fh = open( self.tmpfile, 'rb' )
        new =  [ x for x in enumerate( self.fh.readlines() ) ][ self.last: ]
        for n, i in new:
            line = self._clean( i ).split( '\n' )
            previous = ''
            exline = [ i for i in enumerate( line ) ][ self.llast+1: ]
            for m, l in exline:
                if 'I beg your pardon?' in l and ( previous in ( '> ', '' ) ):
                    continue
                
                previous = l
                if l[ 0 ] == '>':
                    continue
                yield l 
                self.llast = m
            

        self.fh.close()


usage = '''interface.py [gblorb file]'''

if __name__ == '__main__':
    if len( sys.argv ) != 2:
        print( usage )
    else:
        iffile = sys.argv[ 1 ]
        i = i7Game( iffile, interactive=False )

        print( i.intro() )
        cmd = ''
        while cmd != 'quit':
            cmd = input( '--> ' )
            print( i.next( cmd ) )
        
