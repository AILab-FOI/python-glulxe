# python-glulxe
Python 3 interface to glulxe interactive fiction interpreter
------------------------------------------------------------

*python-glulxe* is a Python3 interface to the glulxe interactive fiction interpreter using the .gblorb game file format. You can generate .gblorb files using Inform 7 but you probably know that since you are here ;-)

Installation
------------

To install use the installation script:

'''
sudo python3 setup.py install
'''

Or, the pip installer:

'''
sudo pip3 install git+https://github.com/AILab-FOI/python-glulxe
'''


Usage
-----

To create an instance of an interactive fiction game you want to control using python-gluxle you have to import the i7Game class. To filter the commands given by the user, you have to override the filter method. Here is a quick example in which an alias for the *look* command is created, i.e. if the user types *kuku* the command *look* will be issued. 

'''
#!/usr/bin/env python3
import sys
from glulxe.interface import i7Game

def filter( cmd ):
    if cmd == 'kuku':
        return 'look'
    return cmd

def main( gblorb ):
    game = i7Game( gblorb, interactive=False )
    game.filter = filter
    for output in game.run():
        print( output )
    

if __name__ == '__main__':
    main( sys.argv[ 1 ] )
'''

To run the script you have to provide it with a .gblorb file, i.e.:

'''
python3 example.py mystory.gblorb
'''

You can find more examples in the example folder including using an expert system (dungeon_expert.py), a chatbot (dungeon_chatbot.py), autonomous agents with random actions as well as an ontology based environment generator.