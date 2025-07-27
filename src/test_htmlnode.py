import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_1(self):
        node = HTMLNode("<p>", "This is a paragraph.")
        self.assertEqual(node.props_to_html(), "")
    

    def test_props_to_html_2(self):
        node = HTMLNode("<a>", "This is a link.", None, {"href": "https://boot.dev/"})
        self.assertEqual(node.props_to_html(), ' href="https://boot.dev/"')
    

    def test_props_to_html_3(self):
        node = HTMLNode("<img>", "This is an image.", None, {"src": "https://boot.dev/boots.png", "alt": "Boots the Bear", "width": "128", "height": "128"})
        self.assertEqual(node.props_to_html(), ' src="https://boot.dev/boots.png" alt="Boots the Bear" width="128" height="128"')


    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")
    

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!", {"href": "https://boot.dev/"})
        self.assertEqual(node.to_html(), '<a href="https://boot.dev/">Hello, world!</a>')
    

    def test_leaf_to_html_img(self):
        node = LeafNode("img", "", {"src": "https://boot.dev/boots.png"})
        self.assertEqual(node.to_html(), '<img src="https://boot.dev/boots.png"></img>')


    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    

    def test_to_html_with_anchor(self):
        grandchild_node = LeafNode("a", "grandchild", {"href": "http://boot.dev/"})
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><a href=\"http://boot.dev/\">grandchild</a></span></div>",
        )
    

    def test_to_html_with_img(self):
        grandchild_node = LeafNode("img", "", {"src": "http://boot.dev/boots.png"})
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><img src=\"http://boot.dev/boots.png\"></img></span></div>",
        )