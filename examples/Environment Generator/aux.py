import numpy as np
from owlready2 import *


def testYourLuck(threshold: int = 9, addValue: int = 0, dice: int = 20) -> bool:
    """Function to throw a die (D20 by default) and return true if the die value is over threshold value increased for added value, otherwise false.

    Parameters
    ----------
    threshold : `int`
        Value to test the die against (the default is 17).
    addValue : `int`
        Value to add to the die (the default is 0).
    dice : `int`
        The number of die sides (the default is 20).

    Returns
    -------
    `bool`
        Description of returned object.
    """
    return np.random.randint(1, dice, 1)[0] + addValue > threshold


def chooseFromList(input: list, *args, **kwargs) -> list:
    """Short summary.

    Parameters
    ----------
    input : `list`
        List with elements to choose from.
    *args
        Positional arguments to be forwarded to testYourLuck().
    **kwargs
        Keyword arguments to be forwarded to testYourLuck().

    Returns
    -------
    `list`
        Randomly selected elements of the input list.
    """
    return [item for item in input if testYourLuck(**kwargs)]


def getEntity(entityLabel: str, ontoInstance):
    """Retrieve an ontology entity based on their label.

    Parameters
    ----------
    entityLabel : str
        Label for searching.
    ontoInstance : type
        Owlready2 loaded ontology.
    """
    res = ontoInstance.search(label=entityLabel)
    if len(res) == 1:
        return res[0]
    else:
        return False


def getProperty(label: str, *args, **kwargs):
    return getEntity(label, *args, **kwargs)


def getPropertyValues(property: str, entity, *args, labels: bool = True, **kwargs) -> list:
    """Retrieves elements of extension set of a property by its label.

    Parameters
    ----------
    property : str
        Stored label of the property (rdfs:label).
    entity : owlready2 ontology individual
    labels : bool
        Only the elements' labels will be retrieved (the default is True).

    Returns
    -------
    list
        List of owlready2 individuals or labels.
    """
    try:
        if labels:
            return [v.label[0] for v in getProperty(property, *args, **kwargs)[entity]]
        else:
            return [v for v in getProperty(property, *args, **kwargs)[entity]]
    except Exception as ex:
        print(ex)
        return []
