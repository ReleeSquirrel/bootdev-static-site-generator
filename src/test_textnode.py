import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    

    def test_eq_2(self):
        node = TextNode("This is a text node", TextType.LINK, "https://boot.dev/")
        node2 = TextNode("This is a text node", TextType.LINK, "https://boot.dev/")
        self.assertEqual(node, node2)
    

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    

    def test_not_eq_2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    

    def test_not_eq_3(self):
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.LINK, "https://boot.dev/")
        self.assertNotEqual(node, node2)

    
    def test_not_eq_4(self):
        node = TextNode("This is a text node", TextType.LINK, "https://electricsquirrel.net/")
        node2 = TextNode("This is a text node", TextType.LINK, "https://boot.dev/")
        self.assertNotEqual(node, node2)


    def test_textnode_to_htmlnode_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


    def test_textnode_to_htmlnode_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")


    def test_textnode_to_htmlnode_a(self):
        node = TextNode("This is an anchor node", TextType.LINK, "https://boot.dev/")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is an anchor node")
        self.assertEqual(html_node.props, {"href":"https://boot.dev/"})
    

    def test_textnode_to_htmlnode_img(self):
        node = TextNode("This is an img node", TextType.IMAGE, "https://boot.dev/boots.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src":"https://boot.dev/boots.png", "alt":"This is an img node"})

if __name__ == "__main__":
    unittest.main()