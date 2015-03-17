
import unittest2
import os
import serve
import webtest


class TestServe(unittest2.TestCase):

    def setUp(self):
        self.filename = "delme.p"
        self.serve = serve.Serve(self.filename)
        self.tc = webtest.TestApp(self.serve.get_app())

    def tearDown(self):
        try:
            os.unlink(self.filename)
        except:
            pass

    def test_add_node(self):
        self.tc.post('/items', {"nodeName": "asdf"})
        self.assertIn("asdf", self.tc.get('/'))

    def test_add_two_nodes(self):
        self.tc.post('/items', {"nodeName": "asdf"})
        self.tc.post('/items', {"nodeName": "node2"})
        self.assertIn("asdf", self.tc.get('/'))
        self.assertIn("node2", self.tc.get('/'))

    def test_add_node_clickable(self):
        r = self.tc.get('/')
        r.click("Add node", href="/add")

    def test_add_node(self):
        r = self.tc.get('/add')
        r.form["nodeName"] = "node name"
        redirect = r.form.submit()
        mainPage = redirect.follow()
        self.assertIn("node name", mainPage)

    def xtest_add_page_has_add_button_that_submits_form(self):
        # Filed against webtest as https://github.com/Pylons/webtest/issues/134
        self.fail("don't know how to do this")

    def xtest_add_plus(self):
        self.fail("add+ button should add and redirect back to add page")

    def xtest_node_link(self):
        r = self.tc.get('/add')
        r.form["nodeName"] = "node name"
        redirect = r.form.submit()
        mainPage = redirect.follow()
        self.assertIn("node name", mainPage)
        mainPage.click("node name", href="/nodes/1")
