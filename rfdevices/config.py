import configparser

import pkg_resources

from .device import Protocol, PulseOrder, BasebandValue


config = configparser.ConfigParser()
protocols = {}


def load_config():
    pkg = __name__.split('.')[0]
    resource_dir = 'protocols'

    # can't use os.path.join -- '/' always used for pkg_resources even on windows
    config_resources = ('/'.join([resource_dir, r])
                        for r in pkg_resources.resource_listdir(pkg, resource_dir))

    for config_resource in config_resources:
        config.read_string(pkg_resources.resource_string(pkg, config_resource).decode('utf-8'))

    for section in config.sections():
        proto_config = config[section]
        protocols[section.lower()] = Protocol(
            pulse_length=proto_config.getint('PulseLength'),
            pulse_order=PulseOrder(proto_config.get('PulseOrder')),
            sync=BasebandValue(low=proto_config.getint('SyncLow'),
                               high=proto_config.getint('SyncHigh')),
            zero=BasebandValue(low=proto_config.getint('ZeroLow'),
                               high=proto_config.getint('ZeroHigh')),
            one=BasebandValue(low=proto_config.getint('OneLow'),
                              high=proto_config.getint('OneHigh')),
            message_length=proto_config.getint('MessageLength'),
            repeat=proto_config.getint('Repeat')
        )


def get_protocol(name: str):
    load_config()
    return protocols.get(name.lower(), None)
