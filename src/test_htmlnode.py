import unittest

from htmlnode import HTMLNode


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