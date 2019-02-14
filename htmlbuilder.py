""" a class for containing any tag, containing either
a data, or another tag.
"""
from bs4 import BeautifulSoup


class Tag:
    contents = []
    pretty = True
    attributes = {}

    def __init__(self, item_list, pretty=True):
        self.contents = []
        self.pretty = pretty
        self.name = item_list[0]
        for obj in item_list[1:]:
            if isinstance(obj, list):
                self.contents.append(Tag(obj, pretty))
            elif isinstance(obj, dict):
                self.attributes = obj
            else:
                # probably a string.
                self.contents.append(obj)

    def __str__(self):
        html = "<{}{}>{}</{}>".format(
            self.name,
            self._format_attributes(),
            self._format_contents(),
            self.name,
        )
        if self.pretty:
            return BeautifulSoup(html, features="html.parser").prettify()
        return html

    def _format_attributes(self):
        string = "".join(
            ' {}="{}"'.format(attr, val) for attr, val in zip(
                self.attributes.keys(), self.attributes.values()
            )
        )
        return string

    def _format_contents(self):
        string = "".join(str(item) for item in self.contents)
        return string

    def add(self, item_list):
        """add an element to this tag."""
        self.contents.append(Tag(item_list))
