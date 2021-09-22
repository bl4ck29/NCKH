import configparser, os

parser = configparser.ConfigParser()
parser.read("D:/NCKH/NCKH_PluginMoodle/config.cfg")

def Get(section, option):
    return parser.get(section, option)