import time
import onewire, ds18x20

def rom2str(rom: bytearray) -> str:
    """Strip the crc and put the family code (28) up front. Append the 48 bit serial number."""
    # from docs:
    # 64-BIT LASERED ROM
    # 8-BIT CRC CODE; 48-BIT SERIAL NUMBER; 8-BIT FAMILY CODE
    s = str(hex(int.from_bytes(rom, 'little')))
    # 0x7e0000065cef8f28
    return s[16:18] + s[4:16]


def read_temperatures(ds: ds18x20.DS18X20) -> dict:
    values = {}
    roms = ds.scan()  # scan for sensors on the bus
    ds.convert_temp()  # read temps in °C - need to wait for 750ms
    time.sleep_ms(750)

    for rom in roms:
        serialnum = rom2str(rom)
        values[serialnum] = ds.read_temp(rom)
    return values

