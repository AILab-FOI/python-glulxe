# %% Preliminaries
import argparse
from owlready2 import *
from random import choices, shuffle
import numpy as np
import rdflib
import time
from datetime import datetime
import os
from aux import testYourLuck, getPropertyValues, chooseFromList, getEntity


class Renderer():
    """Short summary.

    Parameters
    ----------
    ontoFile : `str`
        The ontology file (filename and extension) that should be used for rendering.
    ontoPath : `str`
        The path leading to where the ontology file is stored.
    genre : `str`
        Genre of the generated content, must be from the ontology. (the default is 'fantasy').

    Attributes
    ----------
    items : `set`
        A set of rendered items, used for monitoring purposes and avoiding duplicates.
    loadOnto : `def`
        Loads an ontology. This ontology is used by the renderer.
    render : `def`
        The main and root rendering function.
    ontoFile
    ontoPath
    genre

    """

    def __init__(self, ontoFile: str, ontoPath: str, genre: str = 'fantasy'):
        self.ontoFile = ontoFile
        self.ontoPath = ontoPath
        self.genre = genre
        self.items = set()

        self.loadOnto()

        self.render()

    def loadOnto(self, ontoPath: str = None, ontoFile: str = None):
        """Loads an ontology. This ontology is used by the renderer.

        Parameters
        ----------
        ontoPath : `str`
            The path leading to where the ontology file is stored (the default is None).
        ontoFile : `str`
            The ontology file (filename and extension) that should be used for rendering (the default is None).
        """
        if not ontoPath:
            ontoPath = self.ontoPath
        if not ontoFile:
            ontoFile = self.ontoFile

        onto_path.append(ontoPath)
        self.onto = get_ontology(ontoFile)
        self.onto.load()
        with self.onto:
            sync_reasoner_pellet(infer_property_values=True)

        self.graph = default_world.as_rdflib_graph()

        time.sleep(2)

        return

    def renderItem(self, item, containerItem: str = None, supporterItem: str = None, area: str = 'this room'):
        """Renders an item, based on the loaded ontology. If there are items that this item can contain or support, they may be rendered as well and as such.

        Parameters
        ----------
        item : `owlready2 individual`
            The item being rendered.
        containerItem : `str`
            Item wherein the current item is positioned (the default is None).
        supporterItem : `str`
            Item whereon the current item is positioned (the default is None).
        area : `str`
            Area (e.g. room) wherein the current item is located (the default is 'this room').
        """
        props = item.get_properties()
        itemDescriptor = {}
        for p in props:
            try:
                if 'genifi' in p.label[0]:
                    continue
                elif p.label[0] in ['contains', 'can contain', 'supports', 'can support']:
                    itemDescriptor.update({
                        p.label[0]: p[item]
                    })
                else:
                    itemDescriptor.update({
                        p.label[0]: [i.label[0] for i in p[item]]
                    })
            except Exception as ex:
                try:
                    itemDescriptor.update({
                        p.label[0]: p[item]
                    })
                except Exception as ex:
                    itemDescriptor.update({
                        'name': p[item]
                    })

        if len([p for p in itemDescriptor.keys() if p in ['can be on', 'can be placed on', 'can be placed in']]) and not (containerItem or supporterItem):
            return ''

        if 'is plural' in itemDescriptor:
            itemArticle = f"{'Some' if itemDescriptor.get('is plural')[0] else 'A'}"
        else:
            itemArticle = 'A'

        if 'can be of colour' in itemDescriptor:
            itemColour = np.random.choice(
                itemDescriptor.get('can be of colour'))
            if 'can be of material' in itemDescriptor:
                itemMaterial = np.random.choice(
                    itemDescriptor.get('can be of material'))
                itemName = f"{itemColour} {itemMaterial} {itemDescriptor.get('name')[0]}"
            else:
                itemName = f"{itemColour} {itemDescriptor.get('name')[0]}"
        elif 'can be of material' in itemDescriptor:
            itemColour = ''
            itemMaterial = np.random.choice(
                itemDescriptor.get('can be of material'))
            itemName = f"{itemMaterial} {itemDescriptor.get('name')[0]}"
        else:
            itemColour = ''
            itemMaterial = ''
            itemName = itemDescriptor.get('name')[0]

        if itemName in self.items:
            return ''
        else:
            self.items.add(itemName)

        if len(itemDescriptor.get('name')) > 1:
            itemSynonyms = f'" and "{itemColour} {itemMaterial} '.join(
                list(itemDescriptor.get('name'))[1:])
            itemSynonyms = f'Understand "{itemColour} {itemMaterial} {itemSynonyms}" as {itemName}. '
        else:
            itemSynonyms = ''

        if 'has description' in itemDescriptor:
            itemDescription = f'The description of the {itemName} is "' + itemDescriptor.get(
                'has description')[0] + '" '
        else:
            itemDescription = ''

        if 'has property' in itemDescriptor:
            chosenProperties = itemDescriptor.get('has property')
            if 'can have property' in itemDescriptor:
                chosenProperties.extend(chooseFromList(
                    itemDescriptor.get('can have property')))
            itemProperties = 'It is ' + \
                ' and '.join(set(chosenProperties)) + '. '
        else:
            chosenProperties = []
            itemProperties = ''

        if containerItem:
            itemPosition = f'in {containerItem}'
        elif supporterItem:
            itemPosition = f"on {supporterItem}"
        else:
            itemPosition = f'in {area}'

        if 'contains' in itemDescriptor:
            chosenContainedItems = itemDescriptor.get('contains')
        else:
            chosenContainedItems = []
        if 'can contain' in itemDescriptor:
            chosenContainedItems.extend(chooseFromList(
                itemDescriptor.get('can contain')))

        if 'supports' in itemDescriptor:
            chosenSupportedItems = itemDescriptor.get('supports')
        else:
            chosenSupportedItems = []
        if 'can support' in itemDescriptor:
            chosenSupportedItems.extend(chooseFromList(
                itemDescriptor.get('can support')))

        if len(chosenContainedItems) or len(set(chosenProperties).intersection(['open', 'closed', 'openable'])):
            itemType = 'a container '
        elif len(chosenSupportedItems):
            itemType = 'a supporter '
        else:
            itemType = 'a thing '

        itemDefinition = f"{itemArticle} {itemName} is {itemType}{itemPosition}. {itemDescription}{itemProperties}{itemSynonyms}\n"

        for containedItem in chosenContainedItems:
            itemDefinition += self.renderItem(containedItem,
                                              containerItem=itemName)

        for supportedItem in chosenSupportedItems:
            itemDefinition += self.renderItem(supportedItem,
                                              supporterItem=itemName)

        return itemDefinition

    def renderArea(self, area=None, comingFromArea: str = None):
        """Used for rendering the basic description of a room, based on the contents of the loaded ontology. An initial room is chosen on random, and rendered, followed by renderings of all the connected rooms.

        Parameters
        ----------
        area : `owlready2 individual`
            The area to be rendered (the default is None).
        comingFromArea : `str`
            The area that the renderer is coming from, i.e. the one leading to the current area (the default is None).
        """
        areaDescriptor = {}
        for p in area.get_properties():
            try:
                if 'genifi' in p.label[0]:
                    continue
                elif p.label[0] in ['is location of', 'can be location of', 'can be connected to']:
                    areaDescriptor.update({
                        p.label[0]: p[area]
                    })
                else:
                    areaDescriptor.update({
                        p.label[0]: [a.label[0] for a in p[area]]
                    })
            except Exception as e:
                try:
                    areaDescriptor.update({
                        p.label[0]: p[area]
                    })
                except Exception as e:
                    areaDescriptor.update({
                        'name': p[area]
                    })

        areaName = areaDescriptor.get('name')[0]

        if len(areaDescriptor.get('name')) > 1:
            areaSynonyms = f'" and "'.join(
                list(areaDescriptor.get('name')[1:]))
            areaSynonyms = f'Understand "{areaSynonyms}" as {areaName}. '
        else:
            areaSynonyms = ''

        if 'has description' in areaDescriptor:
            areaDescription = f'The description of {areaName} is "' + \
                areaDescriptor.get('has description')[0] + '" '
        else:
            areaDescription = ''

        areaDefinition = f'\n{areaName} is a room. {areaDescription}{areaSynonyms}\n\n'

        if 'is location of' in areaDescriptor:
            chosenItems = areaDescriptor.get('is location of')
        else:
            chosenItems = []
        if 'can be location of' in areaDescriptor:
            chosenItems.extend(chooseFromList([item for item in areaDescriptor.get(
                'can be location of') if item not in chosenItems]))

        for chosenItem in chosenItems:
            areaDefinition += self.renderItem(chosenItem, area=areaName)

        return areaDefinition

    def render(self):

        gameDefinition = """"The L-Space Spurt" by B

Chapter 1 - Setup

Before going a direction (called way) when a room (called next location) is not visited:
    let further place be the room the way from the location;
    if further place is a room, continue the action;
    change the way exit of the location to the next location;
    let reverse be the opposite of the way;
    change the reverse exit of the next location to the location.

Chapter 2 - The World

When play begins:
    say "Prologue.";
    say "           Alice: 'Would you tell me, please, which way I ought to go from here?'";
    say "The Cheshire Cat: 'That depends a good deal on where you want to get to.'";
    say "           Alice: 'I don't much care where.'";
    say "The Cheshire Cat: 'Then it doesn't much matter which way you go.'";
    say "           Alice: '...So long as I get somewhere.'";
    say "The Cheshire Cat: 'Oh, you're sure to do that, if only you walk long enough.'".
        """
        areas = getEntity('Area', ontoInstance=self.onto).instances()
        genreAreas = [a for a in areas if (self.genre in getPropertyValues(
            'is of genre', a, labels=True, ontoInstance=self.onto))]
        selectedArea = np.random.choice(genreAreas)

        # selectedArea = getEntity('Sherwood Forest', ontoInstance=self.onto)
        selectedAreas = [a for a in getPropertyValues(
            'is related to', selectedArea, labels=False, ontoInstance=self.onto)]
        shuffle(selectedAreas)

        print(selectedArea.label[0])

        for area in selectedAreas:
            try:
                gameDefinition += self.renderArea(area)
            except Exception as ex:
                print(ex)
                raise ex

        print(gameDefinition)

        with open(f'RenderedStoryEnv {datetime.now().strftime("%Y%m%d %H:%M:%S")}.ni', 'w') as f:
            f.write(gameDefinition)

        return gameDefinition


def main(genre: str):
    """Main function that instantiates the renderer.

    Parameters
    ----------
    genre : `str`
        Genre of the generated content.
    """
    renderer = Renderer(
        ontoFile='ontology.owx',
        ontoPath=os.path.dirname(os.path.realpath(__file__)),
        genre=genre
    )

    del(renderer)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='A script to generate basic randomised environments based on an ontology containing possible concepts of the in-game world.'
    )
    parser.add_argument("-g", "--genre", type=str,
                        help="Genre of the generated content", default="fantasy")
    args = parser.parse_args()

    main(args.genre)
