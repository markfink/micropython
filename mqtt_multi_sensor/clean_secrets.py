import json
import base64
from config import CONFIG

# keep the config.secrets file secret (don't push to github, don't store on the device, ...)

CONFIG_SECRETS = 'config.secrets'
CONFIG_PY = 'config.py'

def main():
  config = CONFIG
  # read secrets
  with open(CONFIG_SECRETS) as sfile:
    config_secrets = json.load(sfile)

  # add base64 encoded secrets to config
  for key, secret in config_secrets.items():
    config[key] = '<secret>'

  # write back config
  body = 'CONFIG = ' + json.dumps(config, sort_keys=True, indent=2)
  with open(CONFIG_PY, 'w') as cfile:
    cfile.write(body)

  print(f"updating secrets to {CONFIG_PY} completed")


if __name__ == '__main__':
  main()
