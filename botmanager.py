# ################################################################### #
#                                                                     #
#  BigBrotherBot(B3) (www.bigbrotherbot.net)                          #
#  Copyright (C) 2005 Michael "ThorN" Thornton                        #
#                                                                     #
#  This program is free software; you can redistribute it and/or      #
#  modify it under the terms of the GNU General Public License        #
#  as published by the Free Software Foundation; either version 2     #
#  of the License, or (at your option) any later version.             #
#                                                                     #
#  This program is distributed in the hope that it will be useful,    #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of     #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the       #
#  GNU General Public License for more details.                       #
#                                                                     #
#  You should have received a copy of the GNU General Public License  #
#  along with this program; if not, write to the Free Software        #
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA      #
#  02110-1301, USA.                                                   #
#                                                                     #
# ################################################################### #
__author__ = 'donna30' 
__version__ = '1.0'

import b3
import b3.events
import b3.plugin
from threading import Timer

class BotmanagerPlugin(b3.plugin.Plugin):

    requiresConfigFile = False

    bots_enabled = True
    bots_added = False

    def onStartup(self):
        self._adminPlugin = self.console.getPlugin('admin')

        # We cannot start without the admin plugin
        if not self._adminPlugin:
            self.error('Could not find admin plugin')
            return

        # Registering commands
        self._adminPlugin.registerCommand(self, 'enablebots', 60, self.cmd_enablebots)
        self._adminPlugin.registerCommand(self, 'disablebots', 60, self.cmd_disablebots)

        timer = Timer(60, self.checkbots)
        timer.start()

    def checkbots(self):
        bots = 0
        clients = 0

        if self.bots_enabled:
            for client in self.console.clients.getList():
                if client.bot:
                    bots += 1
                else:
                    clients += 1

            if (clients < 3) and not self.bots_added:
                self.console.write("addbot Adrastos 4 blue 489 Megadeth")
                self.console.write("addbot Adrastos 4 blue 652 Metallica")
                self.console.write("addbot Adrastos 4 red 990 Slayer")
                self.console.write("addbot Adrastos 4 red 200 Anthrax")
                self.console.write("g_bluewave 10")
                self.console.write("g_redwave 10")
                self.bots_added = True

            if clients > 7:
                self.console.write("kick allbots")
                self.console.write("g_bluewave 15")
                self.console.write("g_redwave 15")
                self.bots_added = False

        timer = Timer(60, self.checkbots)
        timer.start()

    def cmd_disablebots(self, data, client, cmd=None):
        self.console.write("kick allbots")
        self.console.say("^5Bots ^3[^1Disabled^3]")
        self.enabled = False
        self.bots_added = False
        self.checkbots()

    def cmd_enablebots(self, data, client, cmd=None):
        self.console.say("^5Bots ^3[^2Enabled^3]")
        self.enabled = True
        self.bots_added = True
        self.checkbots()