import re

from enum import Enum

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    delete_list = []
    for i in range(0, len(blocks)):
        if blocks[i] == "\n" or blocks[i] == "":
            delete_list.append(i)
        else:
            blocks[i] = blocks[i].strip()
    for i in range(len(delete_list) - 1, -1, -1):
        del blocks[delete_list[i]]
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


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        node = text_node_to_html_node(text_node)
        html_nodes.append(node)
    return html_nodes


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def ordered_list_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for i in range(0, len(items)):
        text = items[i]
        text = text.removeprefix(f"{i+1}. ")
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def unordered_list_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


