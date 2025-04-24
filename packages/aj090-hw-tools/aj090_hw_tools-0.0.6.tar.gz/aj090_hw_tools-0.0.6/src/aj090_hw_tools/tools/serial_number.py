import asyncio
import logging
import subprocess
import sys
import tempfile
import re
import esptool
import time

from esptool.cmds import detect_chip
from rich.console import Console

from ..common.const import SERIAL_NUM_PATTERN

__all__ = [
    'serial'
]

# Logger 
FORMAT = '%(name)s:%(levelname)s: %(message)s'
logging.basicConfig(level=logging.ERROR, format=FORMAT)
logger = logging.getLogger(__name__)

console = Console()

def nvs_partition_template(factory_mode: bool, hw_version: str, serial_number: str) -> str:
    return """key,type,encoding,value
factory,namespace,,
factory_mode,data,u8,{factory_mode}
hw_version,data,string,{hw_version}
serial,data,string,{serial_number}
""".format(
    factory_mode  = int(factory_mode),
    hw_version    = hw_version,
    serial_number = serial_number
)

async def nvs_write(device, bin_file: str, offset: int = 0x11000) -> None:
    def _write():
        command = ['write_flash', f'{offset}', f'{bin_file}']
        logger.debug("Using command ", " ".join(command))
        esptool.main(command, device)

    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _write) 

async def serial_write(device, serial: str) -> int:
    match = re.search(SERIAL_NUM_PATTERN, serial)
    if match is None:
        console.print('Wrong serial number format', style='bold red')
        return -1
    serial = match.group(0)
    with tempfile.NamedTemporaryFile(suffix='.csv') as nvs_csv:
        data = bytes(nvs_partition_template(True, '1.0', serial).encode())
        nvs_csv.write(data)
        nvs_csv.seek(0)
        logger.debug(f'CSV file data: {nvs_csv.read()}')

        with tempfile.NamedTemporaryFile(suffix='.bin') as nvs_bin:
            args   = ['generate', nvs_csv.name, nvs_bin.name, '0x10000']
            result = subprocess.run([sys.executable, '-m', 'esp_idf_nvs_partition_gen'] + args).returncode
            if not result:
                await nvs_write(device, nvs_bin.name)
            else:
                console.print('NVS partition generate error', style='bold red')
                return -1
    
    console.print('SUCCESS', style='bold green')

async def serial_read() -> int:
    return -1

def serial(argv) -> int:
    port     = argv.port if argv.port is not None else esptool.ESPLoader.DEFAULT_PORT
    connects = 10 # NOTE: the workaround to the issue "Could not open /dev/tty..., the port is busy or doesn't exist" 
    for _ in range(connects): 
        try:   
            with detect_chip(port=port, connect_attempts=0) as device:
                match argv.operation:
                    case 'write':
                        return asyncio.run(serial_write(device, argv.serial))
                    case 'read':
                        return asyncio.run(serial_read(device))
                    case _:
                        console.print('Unknown command', style='red bold')
                        return -1
        except OSError:
            # NOTE: we are trying to close an already closed port (in device_test()), 
            # thus an OSError occurs (invalid file descriptor)
            return 0
        except esptool.util.FatalError as err:
            logger.debug(err)
            time.sleep(1.0)
    print("Can't connect to the device")
    return -1


    