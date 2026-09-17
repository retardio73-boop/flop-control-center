import argparse
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from core.config import load_config, root_path
from core.public_snapshot import build
from core.continuity_journal import append_record, build_record


def main():
    parser = argparse.ArgumentParser(description='Record one bounded continuity observation.')
    parser.add_argument('--journal', help='Override configured continuity journal path.')
    parser.add_argument('--boot-id', default=os.environ.get('FLOP_BOOT_ID'))
    args = parser.parse_args()

    cfg = load_config()
    snap = build(cfg)
    continuity_cfg = cfg.get('continuity', {})
    journal = args.journal or continuity_cfg.get('journal')
    if not journal:
        raise SystemExit('continuity.journal is not configured')
    path = Path(journal)
    if not path.is_absolute():
        path = root_path(cfg) / path
    record = build_record({'tasks': snap.get('tasks', []), 'network': snap.get('network', {})}, boot_id=args.boot_id)
    append_record(path, record)
    print(json.dumps({'ok': True, 'journal': str(path), 'record': record}, indent=2))


if __name__ == '__main__':
    main()
