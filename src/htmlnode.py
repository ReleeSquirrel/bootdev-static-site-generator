



class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):   
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    

    def __repr__(self):
        result = []
        if self.tag:
            result.append(f'HTMLNode tag="{self.tag}"')
        if self.value:
            result.append(f'value="{self.value}"')
        if self.children:
            children_string = 'children="'
            for child in self.children:
                children_string = f"{children_string}{child}"
            children_string = children_string + '"'
            result.append(f'children="{children_string}"')
        if self.props:
            props_string = 'props="'
            for prop in self.props.keys():
                props_string = f'{props_string}"{prop}"="{self.props[prop]}"'
            props_string = props_string + '"'
            result.append(f'props="{self.props}"')
        
        return " ".join(result)
    

    def to_html(self):
        raise NotImplementedError()
    

    def props_to_html(self):
        result = ""
        if self.props:
            for prop in self.props.keys():
                result = result + f' {prop}="{self.props[prop]}"'
        return result


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):   
        super().__init__(tag=tag, value=value, props=props)
    

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag == None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


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