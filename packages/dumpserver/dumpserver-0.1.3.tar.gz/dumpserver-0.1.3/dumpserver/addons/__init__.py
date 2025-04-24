from dumpserver.addons import anticache
from dumpserver.addons import anticomp
from dumpserver.addons import block
from dumpserver.addons import blocklist
from dumpserver.addons import browser
from dumpserver.addons import clientplayback
from dumpserver.addons import command_history
from dumpserver.addons import comment
from dumpserver.addons import core
from dumpserver.addons import cut
from dumpserver.addons import disable_h2c
from dumpserver.addons import export
from dumpserver.addons import next_layer
from dumpserver.addons import onboarding
from dumpserver.addons import proxyserver
from dumpserver.addons import proxyauth
from dumpserver.addons import script
from dumpserver.addons import serverplayback
from dumpserver.addons import mapremote
from dumpserver.addons import maplocal
from dumpserver.addons import modifybody
from dumpserver.addons import modifyheaders
from dumpserver.addons import stickyauth
from dumpserver.addons import stickycookie
from dumpserver.addons import save
from dumpserver.addons import tlsconfig
from dumpserver.addons import upstream_auth


def default_addons():
    return [
        core.Core(),
        browser.Browser(),
        block.Block(),
        blocklist.BlockList(),
        anticache.AntiCache(),
        anticomp.AntiComp(),
        clientplayback.ClientPlayback(),
        command_history.CommandHistory(),
        comment.Comment(),
        cut.Cut(),
        disable_h2c.DisableH2C(),
        export.Export(),
        onboarding.Onboarding(),
        proxyauth.ProxyAuth(),
        proxyserver.Proxyserver(),
        script.ScriptLoader(),
        next_layer.NextLayer(),
        serverplayback.ServerPlayback(),
        mapremote.MapRemote(),
        maplocal.MapLocal(),
        modifybody.ModifyBody(),
        modifyheaders.ModifyHeaders(),
        stickyauth.StickyAuth(),
        stickycookie.StickyCookie(),
        save.Save(),
        tlsconfig.TlsConfig(),
        upstream_auth.UpstreamAuth(),
    ]
