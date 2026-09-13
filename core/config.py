import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
LOCAL = HERE / 'config' / 'config.local.json'
EXAMPLE = HERE / 'config' / 'config.example.json'


def load_config():
    path = LOCAL if LOCAL.exists() else EXAMPLE
    data = json.loads(path.read_text(encoding='utf-8'))
    data['_config_path'] = str(path)
    data['_root'] = str(Path(data['root']).expanduser())
    return data


def root_path(cfg):
    return Path(cfg['_root'])
