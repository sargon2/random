
import pickle
import os
import types

class Node(object):
    def __init__(self, nodeType=None):
        self.nodeType = nodeType

    def setTags(self, tags):
        solo_types = [types.StringTypes, Tag]
        for solo_type in solo_types:
            if isinstance(tags, solo_type):
                tags = [tags]
                break
        self.tags = tags

    def getType(self):
        return self.nodeType

    def getTags(self):
        return self.tags

class Tag(object):
    def __init__(self, name, value = None):
        self.name = name
        self.value = value

    def getName(self):
        return self.name

    def getValue(self):
        return self.value


class DB(object):
    def __init__(self, file_location):
        self.file_location = file_location
        self.db = {}
        if os.path.isfile(self.file_location):
            self.db = pickle.load(open(self.file_location, "rb"))

    def addNode(self, node, nid):
        self.db[nid] = node
        pickle.dump(self.db, open(self.file_location, "wb"))

    def getNodeById(self, nid):
        return self.db[nid]

    def get_storage_location(self):
        return self.file_location
