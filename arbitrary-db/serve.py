
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
        tags = [db.Tag("name", name)]
        if "tags" in flask.request.form:
            in_tags = flask.request.form["tags"]
            tags.append(db.Tag(in_tags))
        n.setTags(tags)
        self.db.addNode(n)
        return flask.redirect("/")

    def addNodePage(self):
        return """
<form action="/items" method="POST">
<input type="text" name="nodeName"/>
<input type="text" name="tags"/>
<input type="submit"/>
</form>
"""

    def get_app(self):
        app = flask.Flask(__name__)
        app.add_url_rule('/', view_func=self.index)
        app.add_url_rule('/items', view_func=self.addNodeToDB, methods=["POST"])
        app.add_url_rule('/add', view_func=self.addNodePage)
        app.add_url_rule('/nodes/<int:nodeid>', view_func=self.nodePage)
        return app

    def nodePage(self, nodeid):
        node = self.db.getNodeById(nodeid)
        ret = node.getTagValue("name")
        ret += "<br />\n"
        for tag in node.getTags():
            ret += "tag: " + tag.getName()
        return ret

    def add_items(self, items):
        self.items.extend(items)

# Untested:
if __name__ == "__main__":
    Serve("db.p").get_app().run(host="0.0.0.0", port=12345)
