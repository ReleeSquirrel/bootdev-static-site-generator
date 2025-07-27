from htmlnode import HTMLNode



class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
    

    def to_html(self):
        if self.tag == None:
            raise ValueError("All ParentNode must have a tag")
        if self.children == None:
            raise ValueError("All ParentNode must have children")
        
        result = ""
        for child in self.children:
            result = result + child.to_html()
        
        return f"<{self.tag}{self.props_to_html()}>{result}</{self.tag}>"