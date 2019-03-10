from utils.common.helpers import set_config, activate_virtual_environment, set_localization

args = set_config('config.json')
set_localization(args)
if args.get('environment') != "":
    activate_virtual_environment(args)
