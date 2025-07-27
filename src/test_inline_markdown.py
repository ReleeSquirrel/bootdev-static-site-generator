import unittest

from inline_markdown import (
    split_nodes_delimiter, extract_markdown_images, extract_markdown_links,
    split_nodes_image, split_nodes_link, text_to_textnodes, extract_title,
)
from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
    def test_bold_at_start(self):
        node = TextNode("**Bold** at start.", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(split_nodes), 2)
        self.assertEqual(split_nodes[0].text, "Bold")
        self.assertEqual(split_nodes[1].text, " at start.")
        self.assertEqual(split_nodes[0].text_type, TextType.BOLD)
        self.assertEqual(split_nodes[1].text_type, TextType.TEXT)


    def test_italics_at_start_bold_in_middle(self):
        node = TextNode("_Italics_ at start. **Bold** in the middle.", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(split_nodes), 3)
        self.assertEqual(split_nodes[0].text, "_Italics_ at start. ")
        self.assertEqual(split_nodes[1].text, "Bold")
        self.assertEqual(split_nodes[2].text, " in the middle.")
        self.assertEqual(split_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(split_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(split_nodes[2].text_type, TextType.TEXT)
        split_nodes = split_nodes_delimiter(split_nodes, "_", TextType.ITALIC)
        self.assertEqual(len(split_nodes), 4)
        self.assertEqual(split_nodes[0].text, "Italics")
        self.assertEqual(split_nodes[1].text, " at start. ")
        self.assertEqual(split_nodes[2].text, "Bold")
        self.assertEqual(split_nodes[3].text, " in the middle.")
        self.assertEqual(split_nodes[0].text_type, TextType.ITALIC)
        self.assertEqual(split_nodes[1].text_type, TextType.TEXT)
        self.assertEqual(split_nodes[2].text_type, TextType.BOLD)
        self.assertEqual(split_nodes[3].text_type, TextType.TEXT)


    def test_code_in_the_middle(self):
        node = TextNode("This string has `code` in the middle.", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(split_nodes), 3)
        self.assertEqual(split_nodes[0].text, "This string has ")
        self.assertEqual(split_nodes[1].text, "code")
        self.assertEqual(split_nodes[2].text, " in the middle.")
        self.assertEqual(split_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(split_nodes[1].text_type, TextType.CODE)
        self.assertEqual(split_nodes[2].text_type, TextType.TEXT)

    
    def test_two_back_to_back_bold_tags(self):
        node = TextNode("This string has two **bold**** things** back to back.", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(split_nodes), 4)
        self.assertEqual(split_nodes[0].text, "This string has two ")
        self.assertEqual(split_nodes[1].text, "bold")
        self.assertEqual(split_nodes[2].text, " things")
        self.assertEqual(split_nodes[3].text, " back to back.")
        self.assertEqual(split_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(split_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(split_nodes[2].text_type, TextType.BOLD)
        self.assertEqual(split_nodes[3].text_type, TextType.TEXT)


    def test_italics_at_end(self):
        node = TextNode("Italics at _end._", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(split_nodes), 2)
        self.assertEqual(split_nodes[0].text, "Italics at ")
        self.assertEqual(split_nodes[1].text, "end.")
        self.assertEqual(split_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(split_nodes[1].text_type, TextType.ITALIC)

    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev/)"
        )
        self.assertListEqual([("link", "https://boot.dev/")], matches)

    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev/) and another [link](http://electricsquirrel.net)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev/"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link", TextType.LINK, "http://electricsquirrel.net"),
            ],
            new_nodes,
        )
    

    def test_text_to_textnodes_1(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        textnodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            textnodes
        )


    def test_text_to_textnodes_2(self):
        text = "**This is all bold**** all of it** **yes even this.**"
        textnodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is all bold", TextType.BOLD),
                TextNode(" all of it", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("yes even this.", TextType.BOLD),
            ],
            textnodes
        )


    def test_extract_title(self):
        text = "# The Title\nThe title is at the start of this string."
        title = extract_title(text)
        self.assertEqual(title, "The Title")

    
 