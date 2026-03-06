import configparser

config = configparser.ConfigParser()
config.read('config.conf')

# 读取配置
def get_config(section_name, key_name):
    return config.get(section_name, key_name)