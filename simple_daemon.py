#!/usr/bin/env python3

import sys
import time
import builtins
from config import args
from utils.common.flags import *
from utils.common.logger import logger
from easy_daemon.daemon import Daemon

_ = builtins.__dict__.get('_', lambda x: x)

# ----------------------------------------------------------------------------------------------------------------------


class ExecApplication:
    @staticmethod
    def run():
        """

        Run application
        Used easy-daemon (https://pypi.org/project/easy-daemon/)

        """
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
    logger.name = args.get('logger_name', sys.argv[0])
    if DEBUG:
        exec_application = ExecApplication()
        exec_application.run()
    else:
        daemon = ExecDaemon(args.get('pid_file', '/tmp/simple_daemon.pid'), logger=logger)
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
