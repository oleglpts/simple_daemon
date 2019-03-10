#!/usr/bin/env python3

import os
import sys
import time
import socket
import signal
import logging
from config import args
from utils.common.flags import *
from utils.common.logger import logger
from easy_daemon.daemon import Daemon
from multiprocessing import cpu_count
from threading import currentThread, Thread
from pooledProcessMixin import PooledProcessMixIn
from socketserver import BaseServer, TCPServer, BaseRequestHandler
from utils.common.helpers import activate_virtual_environment, set_localization

# ----------------------------------------------------------------------------------------------------------------------


class MyTestHandler(BaseRequestHandler):
    """

    Test application that outputs parent process id PPID, PID, thread and client address
    Used easy-daemon (https://pypi.org/project/easy-daemon/)
         pooledProcessMixin (https://pypi.org/project/pooled-ProcessMixIn/)

    """
    def handle(self):
        self.request.settimeout(5.0)
        try:
            data = self.request.recv(1024).strip().decode()
            logger.info("{} wrote: {}".format(self.client_address[0], data))
            self.request.sendall(('PPID=[%d] PID=[%d] thread=[%s] from [%s]: %s\n' % (
                os.getppid(), os.getpid(), currentThread().name, self.client_address[0], data.upper())).encode())
            if data == 'quit':
                logger.info("testing software shutting down.")
                self.server.shutdown()
        except socket.timeout:
            logger.info("{}: reached timeout".format(self.client_address[0]))
            self.request.sendall(('PPID=[%d] PID=[%d] thread=[%s] from [%s]: reached timeout\n' % (
                os.getppid(), os.getpid(), currentThread().name, self.client_address[0])).encode())

# ----------------------------------------------------------------------------------------------------------------------


class MyTCPTest (PooledProcessMixIn, TCPServer):
    """

    Server instance

    """
    def __init__(self, processes=max(2, cpu_count()), threads=64, daemon=False, kill=True, debug=False, log=logger):
        TCPServer.__init__(self, ('127.0.0.1', 8889), MyTestHandler)
        self._process_n = processes
        self._thread_n = threads
        self._daemon = daemon
        self._kill = kill
        self._debug = debug
        self._logger = log
        self._init_pool()
        logger.info("listening on 127.0.0.1:8889")

    @property
    def kill(self):
        return self._kill

# ----------------------------------------------------------------------------------------------------------------------


class ExecApplication:
    @staticmethod
    def run():
        """

        Run application

        """

        def handler(signum, frame):
            """

            SIGTERM handler

            """
            if not (test.kill and test.closed):
                signal.signal(signal.SIGTERM, default_handler)
                test.shutdown()
            time.sleep(1)
            if test.kill:
                Thread(target=BaseServer.shutdown, args=(test,)).start()

        set_localization(args)
        if args.get('environment') != "":
            activate_virtual_environment(args)
        MyTCPTest.allow_reuse_address = True
        test = MyTCPTest(kill=False)
        default_handler = signal.getsignal(signal.SIGTERM)
        signal.signal(signal.SIGTERM, handler)
        test.serve_forever()
        logger.info("Done")

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
        logger.setLevel(logging.DEBUG)
        exec_application = ExecApplication()
        exec_application.run()
    else:
        our_daemon = ExecDaemon(args.get('pid_file', '/tmp/simple_daemon.pid'), logger=logger)
        if len(sys.argv) == 2:
            if 'start' == sys.argv[1]:
                our_daemon.start()
            elif 'stop' == sys.argv[1]:
                our_daemon.stop()
            elif 'restart' == sys.argv[1]:
                our_daemon.restart()
            else:
                print("Unknown command")
                sys.exit(2)
            sys.exit(0)
        else:
            print("usage: %s start|stop|restart" % sys.argv[0])
            sys.exit(2)
