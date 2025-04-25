""" Debugging utilities for pickling and unpickling objects. """
import pickle
import sys
import pprint
from typing import Any
import json

def dump(obj: Any, filename:str ="dump", exit: bool =False) -> None:
    """ Dump pickled object """
    with open(f"{filename}.pickle", "wb") as f:
        pickle.dump(obj, f)
    if exit:
        sys.exit()


def load_dump(filename: str = "dump") -> None:
    """ Load pickled data """
    with open(f"{filename}.pickle", "rb") as f:
        obj = pickle.load(f)
    return obj#, obj_txt

def json_dump (obj: Any, filename: str ="data", exit: bool =False) -> None:
    """ Dump object as JSON """
    with open(f"{filename}.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(obj))
    if exit:
        sys.exit()

def json_load (filename:str="data") -> None:
    """ Load a JSON Object """
    with open(filenane, "r", encoding="utf-8") as f:
        return json.load(f)

