import os
import re
import sys
import site
import json
import gettext
import builtins
import traceback
from utils.common.logger import logger

_ = builtins.__dict__.get('_', lambda x: x)


def activate_virtual_environment(args):
    """

    Activate virtual environment

    :param args: configuration parameters
    :type args: dict

    """
    env = args.get('environment', 'venv')
    env_path = env if env[0:1] == "/" else os.getcwd() + "/" + env
    env_activation = env_path + '/' + 'bin/activate_this.py'
    site.addsitedir(env_path + '/' + args.get('packages', 'lib/python3.5/site-packages'))
    sys.path.append('/'.join(env_path.split('/')[:-1]))
    try:
        exec(open(env_activation).read())
        logger.debug('%s %s %s' % (_('virtual environment'), env_activation, _('activated')))
    except Exception as e:
        logger.critical('%s: (%s)' % (_('virtual environment activation error'), str(e)))
        exit(1)

# ----------------------------------------------------------------------------------------------------------------------


def set_localization(args, quiet=False):
    """

    Install localization

    :param args: command line arguments
    :type args: dict
    :param quiet: if true, print message if translation not found
    :type quiet: bool

    """
    locale_domain = args.get('locale_domain', sys.argv[0])
    locale_dir = args.get('locale_dir', '/usr/share/locale')
    language = args.get('language', 'en')
    gettext.install(locale_domain, locale_dir)
    try:
        gettext.translation(locale_domain, localedir=locale_dir, languages=[language]).install()
        logger.debug('%s for \'%s\' %s' % (_('translation'), language, _('installed')))
    except FileNotFoundError:
        if not quiet:
            logger.warning('%s %s \'%s\' %s, %s' % (
                _('translation'), _('for'), language, _('not found'), _('use default')))

# ----------------------------------------------------------------------------------------------------------------------


def set_config(config_name):
    """

    Config parse

    :param config_name: config file name
    :type config_name: str
    :return parsed config
    :rtype: dict

    """
    try:
        return json.load(open(config_name, 'r'))
    except FileNotFoundError:
        logger.critical('%s %s' % (config_name, _('not found')))
        exit(1)
    except json.JSONDecodeError as error:
        logger.critical('%s %s: %s' % (config_name, _('format error'), str(error)))
        exit(1)

# ----------------------------------------------------------------------------------------------------------------------


def save_config(args):
    """

    Save config

    :param args: parameters
    :type args: dict

    """
    config = open(args.get('config_path', 'config.json'), 'w')
    json.dump(args, config, ensure_ascii=False, indent=4)
    config.close()

# ----------------------------------------------------------------------------------------------------------------------


def error_handler(error, message, sys_exit=False, debug_info=False):
    """

    Error handler

    :param error: current exception
    :type error: Exception or None
    :param message: custom message
    :type message: str
    :param sys_exit: if True, sys.exit(1)
    :type sys_exit: bool
    :param debug_info: if True, output traceback
    :type debug_info: bool

    """
    if debug_info:
        et, ev, tb = sys.exc_info()
        logger.error('%s %s: %s\n%s\n--->\n--->\n' % (
            message, _('error'), error, ''.join(traceback.format_exception(et, ev, tb))))
    else:
        logger.error('%s %s: %s' % (message, _('error'), error))
    if sys_exit:
        logger.error(_('error termination'))
        exit(1)

# ----------------------------------------------------------------------------------------------------------------------


def get_flag(flag_name):
    """

    Get common flag value

    :param flag_name: flag name
    :type flag_name: str
    :return: flag value

    """
    import utils.common.flags
    return getattr(utils.common.flags, flag_name)

# ----------------------------------------------------------------------------------------------------------------------


def set_flag(flag_name, flag_value):
    """

    Set common flag value

    :param flag_name: flag name
    :type flag_name: str
    :param flag_value: flag value

    """
    import utils.common.flags
    setattr(utils.common.flags, flag_name, flag_value)

# ----------------------------------------------------------------------------------------------------------------------


def print_flag(flag_name):
    """

    Print flag value

    :param flag_name: flag name
    :type flag_name: str

    """
    logger.debug(
        '%s %s =  %s' % (_('flag'), flag_name, get_flag(flag_name)))

# ----------------------------------------------------------------------------------------------------------------------


def clear_pool(pool, scanner_name):
    """

    :param pool:
    :param scanner_name:
    :return:
    """
    logger.info('%s %s...' % (scanner_name, _('scanner pool cleaning')))
    pool.shutdown()
    set_flag('TERMINATED', True)

# ----------------------------------------------------------------------------------------------------------------------


def terminating(flag_name, pool=None, scanner_name='', cache=None, key=None, value=None):
    """

    :param flag_name:
    :param pool:
    :param scanner_name:
    :param cache:
    :param key:
    :param value:
    :return:
    """
    print_flag(flag_name)
    result = get_flag(flag_name)
    if result:
        if pool:
            clear_pool(pool, scanner_name)
        if cache:
            cache[key] = value
            cache.close()
    return result

# ----------------------------------------------------------------------------------------------------------------------


def get_modify_date(date_string):
    """

    Search date string

    :param date_string:
    :type date_string: str
    :return: date string
    :rtype: str

    """
    match0 = re.search('\\d{4}-\\d{2}-\\d{2}', date_string)
    match1 = re.search('\\d{2}:\\d{2}:\\d{2}', date_string)
    return date_string[match0.regs[0][0]:match0.regs[0][1]] + ' ' + date_string[match1.regs[0][0]:match1.regs[0][
        1]] if match0 and match1 else None

# ----------------------------------------------------------------------------------------------------------------------


def prepare_path(full_path):
    """

    Prepare directory for file

    :param full_path: full path to file
    :type full_path: str
    :return True if successfully prepared
    :rtype: bool

    """
    path = ''
    for cat in full_path.split('/')[1:-1]:
        path += '/%s' % cat
        if not os.path.exists(path):
            try:
                os.mkdir(path)
                logger.debug('path created: %s' % path)
            except PermissionError:
                logger.critical('there isn\'t permission to create: %s' % path)
                return False
        else:
            logger.debug('path exists: %s' % path)
    return True

# ----------------------------------------------------------------------------------------------------------------------


def translate(message):
    """

    Message translation

    :param message: message
    :type message: str
    :return: translated message

    """
    return builtins.__dict__.get('_', lambda x: x)(message)
