import unittest

from parentnode import ParentNode
from leafnode import LeafNode



class TestParentNode(unittest.TestCase):
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