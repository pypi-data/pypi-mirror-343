from typing import List, TYPE_CHECKING

from dumpserver import connection
from dumpserver.options import Options

if TYPE_CHECKING:
    import dumpserver.proxy.layer


class Context:
    """
    The context object provided to each protocol layer in the proxy core.
    """

    client: connection.Client
    """The client connection."""
    server: connection.Server
    """
    The server connection.

    For practical reasons this attribute is always set, even if there is not server connection yet.
    In this case the server address is `None`.
    """
    options: Options
    """
    Provides access to options for proxy layers. Not intended for use by addons, use `dumpserver.ctx.options` instead.
    """
    layers: List["dumpserver.proxy.layer.Layer"]
    """
    The protocol layer stack.
    """

    def __init__(
        self,
        client: connection.Client,
        options: Options,
    ) -> None:
        self.client = client
        self.options = options
        self.server = connection.Server(None)
        self.layers = []

    def fork(self) -> "Context":
        ret = Context(self.client, self.options)
        ret.server = self.server
        ret.layers = self.layers.copy()
        return ret

    def __repr__(self):
        return (
            f"Context(\n"
            f"  {self.client!r},\n"
            f"  {self.server!r},\n"
            f"  layers=[{self.layers!r}]\n"
            f")"
        )
