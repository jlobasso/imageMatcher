import configparser

config = configparser.ConfigParser()
vard = config.read('conf.ini')

# for attr in dir(config):
#     print("obj.%s = %r" % (attr, getattr(config, attr)))

print(vard)