#
# core.py
#
# Copyright (C) 2011 Jamie Lennox <jamielennox@gmail.com>
#
# Basic plugin template created by:
# Copyright (C) 2008 Martijn Voncken <mvoncken@gmail.com>
# Copyright (C) 2007-2009 Andrew Resch <andrewresch@gmail.com>
# Copyright (C) 2009 Damien Churchill <damoxc@gmail.com>
# Copyright (C) 2010 Pedro Algarvio <pedro@algarvio.me>
#
# Deluge is free software.
#
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# deluge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with deluge.    If not, write to:
# 	The Free Software Foundation, Inc.,
# 	51 Franklin Street, Fifth Floor
# 	Boston, MA  02110-1301, USA.
#
#    In addition, as a special exception, the copyright holders give
#    permission to link the code of portions of this program with the OpenSSL
#    library.
#    You must obey the GNU General Public License in all respects for all of
#    the code used other than OpenSSL. If you modify file(s) with this
#    exception, you may extend this exception to your version of the file(s),
#    but you are not obligated to do so. If you do not wish to do so, delete
#    this exception statement from your version. If you delete this exception
#    statement from all source files in the program, then also delete it here.
#

from deluge.log import LOG as log
from deluge.plugins.pluginbase import CorePluginBase
import deluge.component as component
import deluge.configmanager
from deluge.core.rpcserver import export

from twisted.internet import reactor
from twisted.manhole.telnet import ShellFactory

DEFAULT_PREFS = {
    'username' : 'admin', 
    'password' : 'admin', 
    'port' : 41111,
}

class Core(CorePluginBase):

    def __init__(self, *args, **kwargs): 
        CorePluginBase.__init__(self, *args, **kwargs)
        self.listenport = None

    def enable(self):
        log.debug ("Manhole: Enabled")
        self.config = deluge.configmanager.ConfigManager("manhole.conf", DEFAULT_PREFS)

        sf = ShellFactory()
        sf.username = self.config['username']
        sf.password = self.config['password']

        self.listenport = reactor.listenTCP(self.config['port'], sf)

    def disable(self):
        log.debug ("Manhole: Disabled")

        if self.listenport: 
            self.listenport.stopListening()
            self.listenport = None

    def update(self):
        pass

    @export
    def set_config(self, config):
        """Sets the config dictionary"""
        for key, val in config.iteritems():
            self.config[key] = val
        self.config.save()

    @export
    def get_config(self):
        """Returns the config dictionary"""
        return self.config.config

