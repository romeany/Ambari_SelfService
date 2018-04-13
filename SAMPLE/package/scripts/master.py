import sys, os
from resource_management import *
from resource_management.core.exceptions import ComponentIsNotRunning
from resource_management.core.environment import Environment
from resource_management.core.logger import Logger

class Master(Script):
    def install(self, env):
        print "Install My Master"

    def configure(self, env):
        print "Configure My Master"

    def start(self, env):
        print "Start My Master"

    def stop(self, env):
        print "Stop My Master"

    def status(self, env):
        print "Status..."

if __name__ == "__main__":
    Master().execute()
