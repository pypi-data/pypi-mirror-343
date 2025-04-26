from .symbol import Symbol
from ..markdown import CustomMarkdown
from ..rst import CustomRst

class MD(CustomMarkdown):
    def to_md(self, inner, symbol, parent):
        return "\n\n"

class RST(CustomRst):
    def to_rst(self, inner, symbol, parent):
        return "\n\n"

class Br(Symbol):
    html = "br"
    md = MD()
    rst = RST()
    type = "void"