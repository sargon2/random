
import unittest2
import flask

# TODO:
# The default page should tell you if there are no nodes.
# The default page should have a way to add a node.
# If there's at least one node, the default page should provide you a way to get to at least one node.
# If there are 10 trillion nodes, the default page should not show all 10 trillion.
# If you click a link on the default page to a node, you should get the node page.
# The node page should contain a list of tags.
# The node page should contain the node type.
# The default page should give you a way to (filter?) by node type.
# If a node page shows a tag that contains a list of nodes, you should be able to click those nodes to get to their node pages.

class TestServe(unittest2.TestCase):

    def assertNotNone(self, item):
        self.assertNotEqual(item, None)

    def test_something(self):
        indexstr="asdf"
        app = flask.Flask(__name__)
        def index():
            return indexstr
        app.add_url_rule('/', view_func=index)

        tc = app.test_client()
        result = tc.get('/')
        self.assertIn(indexstr, result.data)
