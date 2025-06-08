import yaml
import time

def config_loader(path):
    with open(path, 'r') as stream:
        src_cfgs = yaml.safe_load(stream)
    return src_cfgs

def format_time(timestamp: float) -> str:
    local_time = time.localtime(timestamp)
    return time.strftime('%H:%M:%S', local_time)