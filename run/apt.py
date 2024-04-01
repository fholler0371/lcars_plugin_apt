import sys
if __name__ == '__main__':
    BASE_PATH = sys.argv[1]
    del sys.argv[1]
else:
    BASE_PATH = None
import asyncio
import argparse


async def main() -> None:
    parser = argparse.ArgumentParser(prog='lcars-apt',
                                     description='Apt-Tool')
    parser.add_argument('--update', action="store_true", dest='update', help='startet apt update')
    parser.add_argument('--upgrade', action="store_true", dest='upgrade', help='startet apt upgrade')
    args = parser.parse_args()
    if args.update:
        print('starte apt update')
        file = sys.argv[0].replace('/apt.', '/run.')
        p = await asyncio.subprocess.create_subprocess_shell(f'{sys.executable} {file} {BASE_PATH}', 
                                                                    stderr=asyncio.subprocess.PIPE, 
                                                                    stdout=asyncio.subprocess.PIPE)
        await p.wait()
    if args.upgrade:
        p = await asyncio.subprocess.create_subprocess_shell('sudo apt upgrade -y')
        await p.wait()
    
if __name__ == "__main__":
    asyncio.run(main())