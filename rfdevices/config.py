import configparser
import re
import typing

import pkg_resources

from .transmitter import Protocol, PulseOrder, BasebandValue


config = configparser.ConfigParser()
# don't lowercase key names
config.optionxform = lambda opt: opt

protocols = {}
codes = {}

CODES_SECTION_RE = re.compile('^codes-', flags=re.IGNORECASE)
CODE_KEY_RE = re.compile('^Code', flags=re.IGNORECASE)


def load_config():
    pkg = __name__.split('.')[0]
    resource_dir = 'protocols'

    # can't use os.path.join -- '/' always used for pkg_resources even on windows
    config_resources = ('/'.join([resource_dir, r])
                        for r in pkg_resources.resource_listdir(pkg, resource_dir))

    for config_resource in config_resources:
        config.read_string(pkg_resources.resource_string(pkg, config_resource).decode('utf-8'))

    proto_sections = []
    for section in config.sections():
        if CODES_SECTION_RE.match(section):
            codes[CODES_SECTION_RE.sub('', section)] = dict((CODE_KEY_RE.sub('', k), v)
                                                            for k, v in config[section].items())
        else:
            proto_config = config[section]
            proto_codes = dict((CODE_KEY_RE.sub('', k), v)
                               for k, v in proto_config.items()
                               if not k.lower() == 'codes' and CODE_KEY_RE.match(k))
            if proto_codes:
                codes[section.lower()] = proto_codes

            proto_sections.append(section)

    for section in proto_sections:
        proto_config = config[section]

        proto_codes = {}
        if 'Codes' in proto_config:
            proto_codes.update(codes[proto_config.get('Codes').lower()])
        if section.lower() in codes:
            proto_codes.update(codes[section.lower()])

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
            repeat=proto_config.getint('Repeat'),
            codes=proto_codes)


def get_protocol(name: str) -> typing.Optional[Protocol]:
    load_config()
    return protocols.get(name.lower(), None)
