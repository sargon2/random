
import unittest2
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
    def __init__(self, value = None):
        self.value = value

    def getValue(self):
        return self.value

class TestSomething(unittest2.TestCase):
    def test_node_exists(self):
        Node()

    def test_node_has_type(self):
        self.assertEquals("nodeType", Node("nodeType").getType())
        self.assertEquals("nodeType2", Node("nodeType2").getType())

    def test_node_has_tag(self):
        n = Node()
        n.setTags("tag1")
        tags = n.getTags()
        self.assertEquals(1, len(tags))
        self.assertEquals("tag1", tags[0])

    def test_node_has_tags(self):
        n = Node()
        n.setTags(["tag1", "tag2"])
        tags = n.getTags()
        self.assertEquals(2, len(tags))
        self.assertEquals("tag1", tags[0])
        self.assertEquals("tag2", tags[1])

    def verifyTagValue(self, val):
        n = Node()
        t = Tag(val)
        n.setTags(t)
        tags = n.getTags()
        self.assertEquals(val, tags[0].getValue())

    def test_tags_can_have_values(self):
        self.verifyTagValue("value!")
        self.verifyTagValue(3)
        self.verifyTagValue(3.2)
        self.verifyTagValue([Node(), Node()])

    def test_persistence_with_reload(self):
        self.fail("Not written yet")
