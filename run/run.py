import pathlib
import tomllib
import asyncio
import sys
import yaml


async def main(base_folder:str) -> None:
    p = await asyncio.subprocess.create_subprocess_shell(f'apt-get update', 
                                                                stderr=asyncio.subprocess.PIPE, 
                                                                stdout=asyncio.subprocess.PIPE)
    await p.wait()
    p = await asyncio.subprocess.create_subprocess_shell(f'apt-get -q -y --ignore-hold --allow-change-held-packages --allow-unauthenticated -s dist-upgrade', 
                                                                stderr=asyncio.subprocess.PIPE, 
                                                                stdout=asyncio.subprocess.PIPE)
    out, err = await p.communicate()
    count = None
    try:
        for line in out.decode().split('\n'):
            line_split = line.split(' ')
            if len(line_split) > 1 and line_split[1] == 'aktualisiert,':
                count = int(line_split[0])
    except:
        return
    config_file = pathlib.Path(base_folder) / 'config' / 'config.toml'
    try:
        with config_file.open('rb') as f:
            cfg = tomllib.load(f)
    except:
        return
    data_file = pathlib.Path(base_folder) / cfg.get('folder', {}).get('data', '') / 'apt.yaml'
    out = {'update_count': count}
    with data_file.open('w') as outfile:
        yaml.dump(out, outfile, default_flow_style=False)
    print('success')
    
if __name__ == '__main__':
    asyncio.run(main(sys.argv[1]))
