import json

with open('config.json') as f:
    cfg = json.load(f)

start_url = cfg['url']

depth = cfg['depth']
dw_other = cfg['dw_from_other_sources']
min_sleep = cfg['wait_between_requests']['min']
max_sleep = cfg['wait_between_requests']['max']
allowed_paths = cfg['allowed_paths']