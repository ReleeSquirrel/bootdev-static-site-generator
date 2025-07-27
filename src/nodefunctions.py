import re
from enum import Enum

from textnode import TextType, TextNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        # If the node isn't a TEXT type node
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        # If the delimiter doesn't appear in the node's text
        elif not delimiter in node.text:
            new_nodes.append(node)
        # Check for closing delimiters; delimiter count should be even
        elif node.text.count(delimiter) % 2 != 0:
            raise Exception("Invalid Markdown Syntax; missing delimiter")
        else:
            result = []
            split_strings = node.text.split(delimiter)
            # tag_toggle is false when the text being analyzed isn't tagged
            tag_toggle = False
            for string in split_strings:
                if string == '':
                    tag_toggle = not tag_toggle
                elif tag_toggle:
                    result.append(TextNode(string, text_type))
                    tag_toggle = not tag_toggle
                else:
                    result.append(TextNode(string, TextType.TEXT))
                    tag_toggle = not tag_toggle
            new_nodes.extend(result)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # If the node isn't a TEXT type node
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            image_links = extract_markdown_images(node.text)
            if len(image_links) == 0:
                new_nodes.append(node)
            else:
                # For each image link found, create nodes for the text before the link and for the link
                # until there is no text remaining
                remaining_text = node.text
        
                for i in range(0, len(image_links)):
                    partitioned_text = remaining_text.partition(f"![{image_links[i][0]}]({image_links[i][1]})")
                    if partitioned_text[0] != "":
                        new_nodes.append(TextNode(partitioned_text[0], TextType.TEXT))
                    new_nodes.append(TextNode(image_links[i][0], TextType.IMAGE, image_links[i][1]))
                    remaining_text = partitioned_text[2]
                if remaining_text != "":
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes
                    

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # If the node isn't a TEXT type node
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            if len(links) == 0:
                new_nodes.append(node)
            else:
                # For each link found, create nodes for the text before the link and for the link
                # until there is no text remaining
                remaining_text = node.text
        
                for i in range(0, len(links)):
                    partitioned_text = remaining_text.partition(f"[{links[i][0]}]({links[i][1]})")
                    if partitioned_text[0] != "":
                        new_nodes.append(TextNode(partitioned_text[0], TextType.TEXT))
                    new_nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
                    remaining_text = partitioned_text[2]
                if remaining_text != "":
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    nodes_list = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    nodes_list = split_nodes_delimiter(nodes_list, "_", TextType.ITALIC)
    nodes_list = split_nodes_delimiter(nodes_list, "`", TextType.CODE)
    nodes_list = split_nodes_image(nodes_list)
    nodes_list = split_nodes_link(nodes_list)
    return nodes_list


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    delete_list = []
    for i in range(0, len(blocks)):
        if blocks[i] == "\n" or blocks[i] == "":
            delete_list.append(i)
        else:
            blocks[i] = blocks[i].strip()
    for i in delete_list:
        del blocks[i]
    return blocks


def block_to_block_type(markdown):
    if markdown.startswith("###### "):
        return BlockType.HEADING
    if markdown.startswith("##### "):
        return BlockType.HEADING
    if markdown.startswith("#### "):
        return BlockType.HEADING
    if markdown.startswith("### "):
        return BlockType.HEADING
    if markdown.startswith("## "):
        return BlockType.HEADING
    if markdown.startswith("# "):
        return BlockType.HEADING
    if markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE
    if markdown.startswith(">") and len(re.findall(r"(\n(?!>))", markdown)) == 0:
        return BlockType.QUOTE
    if markdown.startswith("- ") and len(re.findall(r"(\n(?!- ))", markdown)) == 0:
        return BlockType.UNORDERED_LIST
    # Test for ascending numbers in an ordered list
    ol_test = re.findall(r"(\n\d\. )", markdown)
    ol = True
    if len(ol_test) > 0:
        previous_num = 1
        for match in ol_test:
            if match != f"\n{previous_num + 1}. ":
                ol = False
            else:
                previous_num += 1
    if markdown.startswith("1. ") and ol:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
    