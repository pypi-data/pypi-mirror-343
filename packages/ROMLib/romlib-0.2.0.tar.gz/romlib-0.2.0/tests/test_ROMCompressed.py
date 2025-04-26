import pytest
import sys, os
from pathlib import Path
import shutil

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))

from romlib.roms import ROMcompressed

@pytest.fixture
def rc():
    return ROMcompressed()

def test_getCompressedFileList(rc):
    rc.getCompressedFileList('tests/public_domain_ROMs/snes.zip')
    assert rc.file_list == ['Cannons (v01) (PD).sfc', 'Illusion Intro (PD).sfc']

def test_compressed_type(rc):
    rc.getCompressedFileList('tests/public_domain_ROMs/snes.zip')
    assert rc.compressed_type == "zip"

def test_main_compressed_file(rc):
    rc.getCompressedFileList('tests/public_domain_ROMs/snes.zip')
    assert rc.main_compressed_file == "tests/public_domain_ROMs/snes.zip"

def test_extractFiles_zip_format(rc):

    roms_dir = "tests/public_domain_ROMs/ROMs"

    rc.getCompressedFileList('tests/public_domain_ROMs/snes.zip')
    rc.extractFiles(roms_dir, create_type_directory=True, clean_destination=True)
    exist = [
        os.path.exists("tests/public_domain_ROMs/ROMs/SNES/Cannons (v01) (PD).sfc"),
        os.path.exists("tests/public_domain_ROMs/ROMs/SNES/Illusion Intro (PD).sfc"),
    ]
    assert all(exist)

def test_extractFiles_7z_format_sms(rc):

    roms_dir = "tests/public_domain_ROMs/ROMs"

    rc.getCompressedFileList('tests/public_domain_ROMs/sms.7z')
    rc.extractFiles(roms_dir, create_type_directory=True, clean_destination=False)
    exist = [
        os.path.exists("tests/public_domain_ROMs/ROMs/Master System/Maze3D V2008-01-16 (PD).sms"),
        os.path.exists("tests/public_domain_ROMs/ROMs/Master System/Zoom Effect #1_2 by Charles MacDonald (PD).sms"),
    ]
    assert all(exist)

def test_extractFiles_zip_format_smd(rc):

    roms_dir = "tests/public_domain_ROMs/ROMs"
    rc.getCompressedFileList("tests/public_domain_ROMs/smd.zip")
    rc.extractFiles(roms_dir, create_type_directory=True, clean_destination=False)
    exist = [
        os.path.exists("tests/public_domain_ROMs/ROMs/Mega Drive/DevSter's GALAXIAN! (PD) (32X).32x"),
        os.path.exists("tests/public_domain_ROMs/ROMs/Mega Drive/Flavio's Raster Effects Test (PD).bin"),
    ]
    assert all(exist)

def test_compressIndividually_7z(rc):
    rc.compressIndividually("tests/public_domain_ROMs/ROMs", known_extensions_only=False, file_format="7z", delete_original=True)
    exist = [
        os.path.exists("tests/public_domain_ROMs/ROMs/SNES/Cannons (v01) (PD).7z"),
        os.path.exists("tests/public_domain_ROMs/ROMs/SNES/Illusion Intro (PD).7z"),
        os.path.exists("tests/public_domain_ROMs/ROMs/Mega Drive/DevSter's GALAXIAN! (PD) (32X).7z"),
        os.path.exists("tests/public_domain_ROMs/ROMs/Mega Drive/Flavio's Raster Effects Test (PD).7z"),
    ]
    not_exist = [
        os.path.exists("tests/public_domain_ROMs/ROMs/SNES/Cannons (v01) (PD).sfc"),
        os.path.exists("tests/public_domain_ROMs/ROMs/SNES/Illusion Intro (PD).sfc"),
        os.path.exists("tests/public_domain_ROMs/ROMs/Mega Drive/DevSter's GALAXIAN! (PD) (32X).32x"),
        os.path.exists("tests/public_domain_ROMs/ROMs/Mega Drive/Flavio's Raster Effects Test (PD).bin"),
    ]

    assert all(exist) and not any(not_exist)

def test_decompressIndividually_No_Delete_Original(rc):
    rc.decompressIndividually("tests/public_domain_ROMs/ROMs", delete_original=False)
    exist = [
        os.path.exists("tests/public_domain_ROMs/ROMs/SNES/Cannons (v01) (PD).7z"),
        os.path.exists("tests/public_domain_ROMs/ROMs/SNES/Illusion Intro (PD).7z"),
        os.path.exists("tests/public_domain_ROMs/ROMs/Mega Drive/DevSter's GALAXIAN! (PD) (32X).7z"),
        os.path.exists("tests/public_domain_ROMs/ROMs/Mega Drive/Flavio's Raster Effects Test (PD).7z"),
        os.path.exists("tests/public_domain_ROMs/ROMs/SNES/Cannons (v01) (PD).sfc"),
        os.path.exists("tests/public_domain_ROMs/ROMs/SNES/Illusion Intro (PD).sfc"),
        os.path.exists("tests/public_domain_ROMs/ROMs/Mega Drive/DevSter's GALAXIAN! (PD) (32X).32x"),
        os.path.exists("tests/public_domain_ROMs/ROMs/Mega Drive/Flavio's Raster Effects Test (PD).bin"),
    ]

    assert all(exist)

def test_romClassify(rc):
    
    all_files = [str(archivo) for archivo in Path("tests/public_domain_ROMs/ROMs/").rglob('*') if archivo.is_file()]
    
    file_list = []
    for file in all_files:
        _, extension = os.path.splitext(file)
        if extension == ".7z":
            os.remove(file)
        else:
            file_list.append(file)

    print(file_list)

    all_path = "tests/public_domain_ROMs/ROMs/ALL"
    if not os.path.exists(all_path):
        os.mkdir(all_path)

    for file in file_list:
        filename = os.path.basename(file)
        shutil.move(file, os.path.join(all_path, filename))

    rc.romClassify(all_path, "tests/public_domain_ROMs/ROMs/", not_found_prefix="_")

    exist = [
        os.path.exists("tests/public_domain_ROMs/ROMs/SNES/Cannons (v01) (PD).sfc"),
        os.path.exists("tests/public_domain_ROMs/ROMs/SNES/Illusion Intro (PD).sfc"),
        os.path.exists("tests/public_domain_ROMs/ROMs/Mega Drive/DevSter's GALAXIAN! (PD) (32X).32x"),
        os.path.exists("tests/public_domain_ROMs/ROMs/Mega Drive/Flavio's Raster Effects Test (PD).bin"),
    ]

    not_exist = [
        os.path.exists("tests/public_domain_ROMs/ROMs/SNES/Cannons (v01) (PD).7z"),
        os.path.exists("tests/public_domain_ROMs/ROMs/SNES/Illusion Intro (PD).7z"),
        os.path.exists("tests/public_domain_ROMs/ROMs/Mega Drive/DevSter's GALAXIAN! (PD) (32X).7z"),
        os.path.exists("tests/public_domain_ROMs/ROMs/Mega Drive/Flavio's Raster Effects Test (PD).7z"),
    ]


    assert all(exist) and not any(not_exist)
