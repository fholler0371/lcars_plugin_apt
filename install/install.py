import tomllib
import pathlib
import sys


async def install(parent_cfg: dict) -> dict:
    config_file = pathlib.Path('/'.join(__file__.split('/')[:-2])) / 'config/config.toml'
    cfg = {}
    out = {}
    with config_file.open('rb') as f:
        cfg = tomllib.load(f)
    if 'systemd' in cfg:
        out['systemd'] = []
        for job in cfg['systemd']:
            job['content'] = job['content'].replace('%python%', sys.executable)
            job['content'] = job['content'].replace('%base%', parent_cfg.get('folder', {}).get('base', ''))
            job['content'] = job['content'].replace('%git%', parent_cfg.get('folder', {}).get('base', '')+'/'+parent_cfg.get('folder', {}).get('git', ''))
            out['systemd'].append(job)
    requirements = cfg.get('setup', {}).get('requirements')
    if requirements:
        out['requirements'] = requirements
    return out