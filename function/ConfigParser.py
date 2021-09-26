import configparser

parser = configparser.ConfigParser()
parser.read("/home/vlu-fit/NCKH/config.cfg")

def Get(section, option):
    return parser.get(section, option)
