import os
import sys
import time
import atexit
import signal
from utils.common.logger import logger
from utils.common.helpers import prepare_path

########################################################################################################################
#              Unix daemon basic class (see http://devres.zoomquiet.top/data/20150702154058/index.html)                #
########################################################################################################################


class Daemon:
    """

    Unix daemon basic class

    """

    def __init__(self, pid_file):
        """

        Constructor

        :param pid_file: pid file path
        :type pid_file: str

        """
        self.pid_file = pid_file

    # ------------------------------------------------------------------------------------------------------------------

    def daemonize(self):
        """

        Daemonize application

        """

        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as err:
            sys.stderr.write('fork 1 failed: {0}\n'.format(err))
            sys.exit(1)
        os.chdir('/')
        os.setsid()
        os.umask(0)
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as err:
            sys.stderr.write('fork 2 failed: {0}\n'.format(err))
            sys.exit(1)
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(os.devnull, 'r')
        so = open(os.devnull, 'a+')
        se = open(os.devnull, 'a+')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
        atexit.register(self.delete_pid)
        pid = str(os.getpid())
        prepare_path(self.pid_file)
        with open(self.pid_file, 'w+') as f:
            f.write(pid + '\n')

    # ------------------------------------------------------------------------------------------------------------------

    def delete_pid(self):
        """

        Delete pid file

        """
        os.remove(self.pid_file)

    # ------------------------------------------------------------------------------------------------------------------

    def start(self):
        """

        Start daemon

        """
        try:
            with open(self.pid_file, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None
        if pid:
            message = "pid file {0} already exist. Daemon already running?\n"
            sys.stderr.write(message.format(self.pid_file))
            sys.exit(1)
        self.daemonize()
        logger.info('daemon started')
        self.run()

    # ------------------------------------------------------------------------------------------------------------------

    def stop(self):
        """

        Stop daemon

        """
        try:
            with open(self.pid_file, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None
        if not pid:
            message = "pid file {0} does not exist. Daemon not running?\n"
            sys.stderr.write(message.format(self.pid_file))
            return
        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            e = str(err.args)
            if e.find("No such process") > 0:
                if os.path.exists(self.pid_file):
                    os.remove(self.pid_file)
                    logger.info('daemon stopped')
            else:
                print(str(err.args))
                sys.exit(1)

    # ------------------------------------------------------------------------------------------------------------------

    def restart(self):
        """

        Restart daemon

        """
        self.stop()
        self.start()

    # ------------------------------------------------------------------------------------------------------------------

    def run(self):
        """

        Override it

        """
        raise NotImplementedError("Method 'run' for class 'Daemon' not implemented")
