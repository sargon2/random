
import flask
import db

class Serve(object):
    def __init__(self, db_name):
        self.items = []
        self.db = db.DB(db_name)

    def index(self):
        nodes = self.db.getAllNodes()
        ret = ""
        ret += """<a href="/add">Add node</a><br />\n"""
        for nodeid, node in nodes:
            ret += """<a href="/nodes/{0}">""".format(nodeid)
            ret += node.getTagValue("name")
            ret += "</a>"
            ret += "<br />\n"
        return ret

    def addNodeToDB(self):
        name = flask.request.form["nodeName"]
        n = db.Node()
        n.setTags(db.Tag("name", name))
        self.db.addNode(n)
        return flask.redirect("/")

    def addNodePage(self):
        return """<form action="/items" method="POST"><input type="text" name="nodeName"/><input type="submit"/></form>"""

    def get_app(self):
        app = flask.Flask(__name__)
        app.add_url_rule('/', view_func=self.index)
        app.add_url_rule('/items', view_func=self.addNodeToDB, methods=["POST"])
        app.add_url_rule('/add', view_func=self.addNodePage)
        app.add_url_rule('/nodes/<int:nodeid>', view_func=self.node)
        return app

    def node(self, nodeid):
        node = self.db.getNodeById(nodeid)
        return node.getTagValue("name")

    def add_items(self, items):
        self.items.extend(items)

# Untested:
if __name__ == "__main__":
    Serve("db.p").get_app().run(host="0.0.0.0", port=12345)
