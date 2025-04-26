from markupsafe import Markup

from domilite.dom_tag import dom_tag
from domilite.dom_tag import Flags
from domilite.render import RenderStream
from domilite.render import RenderFlags

__all__ = ["container"]


class container(dom_tag):
    flags = Flags.PRETTY | Flags.INLINE

    def _render(self, stream: "RenderStream") -> None:
        inline = self._render_children(stream)
        if RenderFlags.PRETTY in stream.flags and not inline:
            stream.newline()


class text(dom_tag):
    flags = Flags.INLINE

    def __init__(self, text: str, escape: bool = True):
        super().__init__()
        self.escape = escape
        self.text = text

    def _render(self, stream: "RenderStream") -> None:
        if self.escape:
            stream.write(Markup.escape(self.text))
        else:
            stream.write(self.text)
