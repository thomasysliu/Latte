#!/usr/bin/env python3
# coding=utf-8
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import os
import argparse
import signal
import sys
import subprocess
from gi.repository import GObject, Gtk, AppIndicator3 # had to install gir1.2-appindicator3-0.1

# Handle command-line arguments
parser = argparse.ArgumentParser(prog='Latte', description='Prevent desktop idleness')
parser.add_argument('-V', '--version', action='version', version='Latte 1.0.0')
parser.parse_args()

class Latte(GObject.GObject):

    def __init__(self):
        GObject.GObject.__init__(self)
        self.disable_suspend()
        self._add_indicator()
        #signal.signal(signal.SIGINT, self.signal_handler)
        #signal.pause()


    def _add_indicator(self):
        self.AppInd = AppIndicator3.Indicator.new("Latte",
                                                  "Latte",
                                                  AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        self.AppInd.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.AppInd.set_icon(self.get_resource_path("Latte.svg"))
        self._build_indicator_menu(self.AppInd)

    def _build_indicator_menu(self, indicator):
        menu = Gtk.Menu()
        
        menu_item = Gtk.MenuItem("Quit")
        menu.append(menu_item)
        menu_item.connect("activate", self.on_quit)
        menu_item.show()

        indicator.set_menu(menu)

    def on_quit(self, menuitem):
         self.enable_suspend()
         sys.exit(0)

    def disable_suspend(self):
         self.window_id = subprocess.Popen('xwininfo -root | grep xwininfo | cut -d" " -f4', stdout=subprocess.PIPE, shell=True).stdout.read().strip()
         subprocess.call(['xdg-screensaver', 'suspend', self.window_id])
         logging.info("Latte is inhibiting desktop idleness")
         
    def enable_suspend(self):
         subprocess.call(['xdg-screensaver', 'resume', self.window_id])
         logging.info("Latte is resuming desktop idleness")
         
    def signal_handler(self,signal, frame):
        self.enable_suspend()
        sys.exit(0)
        
    def get_resource_path(self,rel_path):
        dir_of_py_file = os.path.dirname(__file__)
        rel_path_to_resource = os.path.join(dir_of_py_file, rel_path)
        abs_path_to_resource = os.path.abspath(rel_path_to_resource)
        return abs_path_to_resource
# Set up and run
logging.basicConfig(level=logging.INFO)
GObject.threads_init()
latte = Latte()
Gtk.main()
