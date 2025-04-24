import typing

from dumpserver import exceptions
from dumpserver import flow
from dumpserver import ctx

from dumpserver.tools.console import overlay
from dumpserver.tools.console import signals


class CommandExecutor:
    def __init__(self, master):
        self.master = master

    def __call__(self, cmd):
        if cmd.strip():
            try:
                ret = self.master.commands.execute(cmd)
            except exceptions.CommandError as e:
                ctx.log.error(str(e))
            else:
                if ret is not None:
                    if type(ret) == typing.Sequence[flow.Flow]:
                        signals.status_message.send(
                            message="Command returned %s flows" % len(ret)
                        )
                    elif type(ret) == flow.Flow:
                        signals.status_message.send(
                            message="Command returned 1 flow"
                        )
                    else:
                        self.master.overlay(
                            overlay.DataViewerOverlay(
                                self.master,
                                ret,
                            ),
                            valign="top"
                        )
