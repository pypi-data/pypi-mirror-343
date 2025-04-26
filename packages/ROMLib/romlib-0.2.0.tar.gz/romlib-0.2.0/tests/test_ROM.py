import pytest
import sys, os
from pathlib import Path
import shutil

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))

from romlib.roms import ROMcompressed, ROMDetector, ROM_SMD, ROM_NES, ROM_SMS

@pytest.fixture
def rd():
    return ROMDetector()

def test_getCompressedFileList(rd):
    rom_type = rd.detectType("tests/public_domain_ROMs/ROMs/Mega Drive/DevSter's GALAXIAN! (PD) (32X).32x")
    assert rom_type == "Mega Drive"

def test_load_SMD(rd):
    romSMD = rd.load("tests/public_domain_ROMs/ROMs/Mega Drive/DevSter's GALAXIAN! (PD) (32X).32x")
    assert \
        romSMD.pretty_data["system_type"] == "SEGA GENESIS" \
        and romSMD.pretty_data.get("rom_checksum", None) != None \
        and romSMD.pretty_data["loaded_class"] == "SMD"
    
def test_SMD(rd):
    romSMD = ROM_SMD()
    romSMD.load("tests/public_domain_ROMs/ROMs/Mega Drive/DevSter's GALAXIAN! (PD) (32X).32x")
    assert romSMD.pretty_data == {'loaded_class': 'SMD', 'system_type': 'SEGA GENESIS', \
                                   'copyright_release_date': '(C)SEGA 2000.DEC', 'title_domestic': '', \
                                    'title_overseas': 'BasiEgaXorz: DevSter`s GALAXIAN!', 'serial_number_full': 'GM MK-0000 -00', 'software_type': 'Game', 'serial_number': 'MK-0000', 'revision': '00', 'rom_checksum': '0000', 'device_support': '3-button controller, 6-button controller', 'rom_size': '4.0 MB', 'ram_size': '2048 KB', 'extra_memory_available': 'no', \
                                        'extra_memory_saves': 'unknown', 'extra_memory_usage': 'unknown', 'modem_support': 'no'}
    
def test_SMS(rd):
    romSMD = ROM_SMS()
    romSMD.load("tests/public_domain_ROMs/ROMs/Master System/Maze3D V2008-01-16 (PD).sms")
    assert romSMD.pretty_data == {'loaded_class': 'SMS', 'system_type': 'TMR SEGA', 'checksum': 'ce35', 'product_code': 24365, 'version': 0, 'region_code': 'SMS Export', 'rom_size': '32 KB', 'codemasters_rom': 'no', 'sdsc_rom': 'no'}
    
def test_NES(rd):
    rc = ROMcompressed()
    rc.getCompressedFileList("tests/public_domain_ROMs/nes.7z")
    rc.extractFiles("tests/public_domain_ROMs/ROMs", create_type_directory=True, clean_destination=False)
    
    romNES = ROM_NES()
    romNES.load("tests/public_domain_ROMs/ROMs/NES/Chopper by Neil Halelamien and Darren Shultz (PD).nes")

    assert romNES.pretty_data == {'romfile_type': 'iNES', 'PRG_ROM_size': '16 KB', 'CHR_ROM_size': '8 KB', 'nametable_arrangement': 'horizontal (vertically mirrored)', 'persistent_memory': 'no', '512_byte_trainer': 'no', 'alternative_nametable': 'no', 'vs_unisystem': 'no', 'playchoice_10': 'no', 'PRG_RAM_size': '8 KB', 'tv_system': 'NTSC', 'mapper_number': 0, 'mapper': 'NROM'}
                                