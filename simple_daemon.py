#!/usr/bin/env python3

import sys
import time
from utils.common.flags import *
from utils.common.daemon import Daemon
from utils.common.logger import logger
from utils.common.helpers import set_config, activate_virtual_environment, set_localization

# ----------------------------------------------------------------------------------------------------------------------


class ExecApplication:
    @staticmethod
    def run():
        """

        Run application

        """
        set_localization(args)
        if args.get('environment') != "":
            activate_virtual_environment(args)
        while True:
            logger.info(_('daemon worked'))
            time.sleep(5)


# ----------------------------------------------------------------------------------------------------------------------


class ExecDaemon(Daemon):
    def run(self):
        """

        Run process

        """
        exec_daemon = ExecApplication()
        exec_daemon.run()

########################################################################################################################
#                                                    Entry point                                                       #
########################################################################################################################


if __name__ == "__main__":
    if DEBUG:
        args = set_config('config.json')
        exec_application = ExecApplication()
        exec_application.run()
    else:
        args = set_config('/etc/simple_daemon/config.json')
        daemon = ExecDaemon(args.get('pid_file', '/var/run/simple_daemon/simple_daemon.pid'))
        if len(sys.argv) == 2:
            if 'start' == sys.argv[1]:
                daemon.start()
            elif 'stop' == sys.argv[1]:
                daemon.stop()
            elif 'restart' == sys.argv[1]:
                daemon.restart()
            else:
                print("Unknown command")
                sys.exit(2)
            sys.exit(0)
        else:
            print("usage: %s start|stop|restart" % sys.argv[0])
            sys.exit(2)
