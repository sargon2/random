
import unittest2
import os

import db

class TestDB(unittest2.TestCase):
    def tearDown(self):
        try:
            os.unlink("testdb.p")
        except:
            pass

    def test_node_exists(self):
        db.Node()

    def test_node_has_type(self):
        self.assertEquals("nodeType", db.Node("nodeType").getType())
        self.assertEquals("nodeType2", db.Node("nodeType2").getType())

    def test_node_has_tag(self):
        n = db.Node()
        n.setTags("tag1")
        tags = n.getTags()
        self.assertEquals(1, len(tags))
        self.assertEquals("tag1", tags[0])

    def test_node_has_tags(self):
        n = db.Node()
        n.setTags(["tag1", "tag2"])
        tags = n.getTags()
        self.assertEquals(2, len(tags))
        self.assertEquals("tag1", tags[0])
        self.assertEquals("tag2", tags[1])

    def verifyTag(self, tagname, val):
        n = db.Node()
        t = db.Tag(tagname, val)
        n.setTags(t)
        tags = n.getTags()
        self.assertEquals(tagname, tags[0].getName())
        self.assertEquals(val, tags[0].getValue())

    def test_tags_can_have_values(self):
        self.verifyTag("tagname", "value!")
        self.verifyTag("tagname2", "value!")
        self.verifyTag("tagname", 3)
        self.verifyTag("tagname", 3.2)
        self.verifyTag("tagname", [db.Node(), db.Node()])

    def test_persistence_with_reload(self):
        n = db.Node("nodetype")
        t = db.Tag("tagname", "value")
        n.setTags(t)
        nid = 1
        db.DB("testdb.p").addNode(n, nid)

        reload(db)

        result = db.DB("testdb.p").getNodeById(nid)
        self.assertEqual("nodetype", result.getType())
        tag = result.getTags()[0]
        self.assertEqual("tagname", tag.getName())
        self.assertEqual("value", tag.getValue())

    def test_db_size_constant(self):
        # save the same node twice, assert the second one doesn't increase size
        n = db.Node("nodetype")
        t = db.Tag("tagname", "value")
        n.setTags(t)
        ndb = db.DB("testdb.p")
        ndb.addNode(n, 1)

        size_before = os.stat(ndb.get_storage_location()).st_size
        self.assertGreater(size_before, 1)

        ndb.addNode(n, 1)
        size_after = os.stat(ndb.get_storage_location()).st_size

        self.assertEqual(size_before, size_after)

    def test_generate_nid(self):
        ndb = db.DB("testdb.p")
        ndb.addNode(db.Node())
        ndb.addNode(db.Node())
        result = db.DB("testdb.p").getAllNodes()
        self.assertEquals(2, len(result))

    def test_get_tag_value(self):
        n = db.Node()
        n.setTags(db.Tag("tag", "value"))
        self.assertEquals("value", n.getTagValue("tag"))
