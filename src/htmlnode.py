



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