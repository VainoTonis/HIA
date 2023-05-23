from yaml import safe_load

with open('config.yaml', 'r') as file:
    globalConfig_data = safe_load(file)

globalConfig = globalConfig_data