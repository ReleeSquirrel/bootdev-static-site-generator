import re

from textnode import TextType, TextNode


def text_to_textnodes(text):
    nodes_list = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    nodes_list = split_nodes_delimiter(nodes_list, "_", TextType.ITALIC)
    nodes_list = split_nodes_delimiter(nodes_list, "`", TextType.CODE)
    nodes_list = split_nodes_image(nodes_list)
    nodes_list = split_nodes_link(nodes_list)
    return nodes_list


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        # If the node isn't a TEXT type node
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        # If the delimiter doesn't appear in the node's text
        if not delimiter in node.text:
            new_nodes.append(node)
            continue
        # Check for closing delimiters; delimiter count should be even
        if node.text.count(delimiter) % 2 != 0:
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


def extract_title(markdown):
    if not "# " in markdown:
        raise Exception("No title in markdown")
    else:
        lines = markdown.split("\n")
        for line in lines:
            if line.startswith("# "):
                return line[2:]


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





