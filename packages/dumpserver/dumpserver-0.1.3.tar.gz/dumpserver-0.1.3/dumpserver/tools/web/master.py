import tornado.httpserver
import tornado.ioloop

from dumpserver import addons
from dumpserver import log
from dumpserver import master
from dumpserver import optmanager
from dumpserver.addons import errorcheck, eventstore
from dumpserver.addons import intercept
from dumpserver.addons import readfile
from dumpserver.addons import termlog
from dumpserver.addons import view
from dumpserver.contrib.tornado import patch_tornado
from dumpserver.tools.web import app, webaddons, static_viewer


class WebMaster(master.Master):
    def __init__(self, options, with_termlog=True):
        super().__init__(options)
        self.view = view.View()
        self.view.sig_view_add.connect(self._sig_view_add)
        self.view.sig_view_remove.connect(self._sig_view_remove)
        self.view.sig_view_update.connect(self._sig_view_update)
        self.view.sig_view_refresh.connect(self._sig_view_refresh)

        self.events = eventstore.EventStore()
        self.events.sig_add.connect(self._sig_events_add)
        self.events.sig_refresh.connect(self._sig_events_refresh)

        self.options.changed.connect(self._sig_options_update)

        if with_termlog:
            self.addons.add(termlog.TermLog())
        self.addons.add(*addons.default_addons())
        self.addons.add(
            webaddons.WebAddon(),
            intercept.Intercept(),
            readfile.ReadFile(),
            static_viewer.StaticViewer(),
            self.view,
            self.events,
            errorcheck.ErrorCheck(),
        )
        self.app = app.Application(
            self, self.options.web_debug
        )

    def _sig_view_add(self, view, flow):
        app.ClientConnection.broadcast(
            resource="flows",
            cmd="add",
            data=app.flow_to_json(flow)
        )

    def _sig_view_update(self, view, flow):
        app.ClientConnection.broadcast(
            resource="flows",
            cmd="update",
            data=app.flow_to_json(flow)
        )

    def _sig_view_remove(self, view, flow, index):
        app.ClientConnection.broadcast(
            resource="flows",
            cmd="remove",
            data=flow.id
        )

    def _sig_view_refresh(self, view):
        app.ClientConnection.broadcast(
            resource="flows",
            cmd="reset"
        )

    def _sig_events_add(self, event_store, entry: log.LogEntry):
        app.ClientConnection.broadcast(
            resource="events",
            cmd="add",
            data=app.logentry_to_json(entry)
        )

    def _sig_events_refresh(self, event_store):
        app.ClientConnection.broadcast(
            resource="events",
            cmd="reset"
        )

    def _sig_options_update(self, options, updated):
        options_dict = optmanager.dump_dicts(options, updated)
        app.ClientConnection.broadcast(
            resource="options",
            cmd="update",
            data=options_dict
        )

    async def running(self):
        patch_tornado()
        # Register tornado with the current event loop
        tornado.ioloop.IOLoop.current()

        # Add our web app.
        http_server = tornado.httpserver.HTTPServer(self.app)
        http_server.listen(self.options.web_port, self.options.web_host)

        self.log.info(
            f"Web server listening at http://{self.options.web_host}:{self.options.web_port}/",
        )

        return await super().running()
