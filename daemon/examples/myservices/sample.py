#
# CORE
# Copyright (c)2010-2012 the Boeing Company.
# See the LICENSE file included in this distribution.
#
"""
Sample user-defined service.
"""

from core.misc.ipaddress import Ipv4Prefix
from core.service import CoreService
from core.service import ServiceManager


class MyService(CoreService):
    """
    This is a sample user-defined service.
    """
    # a unique name is required, without spaces
    _name = "MyService"
    # you can create your own group here
    _group = "Utility"
    # list of other services this service depends on
    _depends = ()
    # per-node directories
    _dirs = ()
    # generated files (without a full path this file goes in the node's dir,
    #  e.g. /tmp/pycore.12345/n1.conf/)
    _configs = ('myservice.sh',)
    # this controls the starting order vs other enabled services
    _startindex = 50
    # list of startup commands, also may be generated during startup
    _startup = ('sh myservice.sh',)
    # list of shutdown commands
    _shutdown = ()

    @classmethod
    def generateconfig(cls, node, filename, services):
        """
        Return a string that will be written to filename, or sent to the
        GUI for user customization.
        """
        cfg = "#!/bin/sh\n"
        cfg += "# auto-generated by MyService (sample.py)\n"

        for ifc in node.netifs():
            cfg += 'echo "Node %s has interface %s"\n' % (node.name, ifc.name)
            # here we do something interesting
            cfg += "\n".join(map(cls.subnetentry, ifc.addrlist))
            break
        return cfg

    @staticmethod
    def subnetentry(x):
        """
        Generate a subnet declaration block given an IPv4 prefix string
        for inclusion in the config file.
        """
        if x.find(":") >= 0:
            # this is an IPv6 address
            return ""
        else:
            net = Ipv4Prefix(x)
            return 'echo "  network %s"' % net


# this is needed to load desired services when being integrated into core, otherwise this is not needed
def load_services():
    # this line is required to add the above class to the list of available services
    ServiceManager.add(MyService)
