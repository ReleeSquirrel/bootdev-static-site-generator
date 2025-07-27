from textnode import TextNode, TextType

def main():
    text_node = TextNode("This is some Anchor Text", TextType.LINK, "https://boot.dev/")
    print(text_node)


main()