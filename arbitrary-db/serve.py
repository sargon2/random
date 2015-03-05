
import flask
import db

# TODO:
# (done) The default page should tell you if there are no nodes.
# The default page should have a way to add a node.
#   How do I assert that we have a clickable add button?
#   (done) post some data
# If there's at least one node, the default page should provide you a way to get to at least one node.
# If there are 10 trillion nodes, the default page should not show all 10 trillion.
# If you click a link on the default page to a node, you should get the node page.
# The node page should contain a list of tags.
# The node page should contain the node type.
# The default page should give you a way to (filter?) by node type.
# If a node page shows a tag that contains a list of nodes, you should be able to click those nodes to get to their node pages.

class Serve(object):
    def __init__(self, db_name):
        self.items = []
        self.db = db.DB(db_name)

    def index(self):
        nodes = self.db.getAllNodes()
        ret = ""
        for node in nodes:
            ret += node.getTagValue("name")
        return ret

    def add(self):
        name = flask.request.form["nodeName"]
        n = db.Node()
        n.setTags(db.Tag("name", name))
        self.db.addNode(n)
        return "added" # TODO: redirect to make f5 cleaner

    def get_app(self):
        app = flask.Flask(__name__)
        app.add_url_rule('/', view_func=self.index)
        app.add_url_rule('/items', view_func=self.add, methods=["POST"])
        return app

    def add_items(self, items):
        self.items.extend(items)

# Untested:
if __name__ == "__main__":
    Serve("db.p").get_app().run(host="0.0.0.0", port=12345)
