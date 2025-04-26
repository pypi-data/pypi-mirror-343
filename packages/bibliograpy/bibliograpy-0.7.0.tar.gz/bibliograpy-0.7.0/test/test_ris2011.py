"""Test module for ris2001."""

from argparse import Namespace
from pathlib import Path
import time

from bibliograpy.process import _process


def _resource(file: str) -> str:
    """Chemin vers les fichiers d'entrée."""
    return str(Path(Path(__file__).parent / 'resources' / file))


def _sibbling_module(file: str) -> str:
    """Chemin vers les fichiers de modules voisins."""
    return str(Path(Path(__file__).parent / file))


def test_to_py():
    """test process from a yml bibliography to a py source bibliography"""

    _process(Namespace(CMD='ris2011',
                       file=_resource('S0301622601003232.ris'),
                       output_file=_sibbling_module('test_ris2011_to_py.py'),
                       encoding='utf-8',
                       output_dir='.'))

    time.sleep(1) # wait for the bibliography source file to be generated

    from test_ris2011_to_py import FIRK_AL_2002

    assert len(FIRK_AL_2002) == 16

def test_vrd2344_to_py():
    """test process from a yml bibliography to a py source bibliography"""

    _process(Namespace(CMD='ris2011',
                       file=_resource('vr.d2344.ris'),
                       output_file=_sibbling_module('test_ris2011_vrd2344_to_py.py'),
                       encoding='utf-8',
                       output_dir='.'))

    time.sleep(1) # wait for the bibliography source file to be generated

    from test_ris2011_vrd2344_to_py import VR_D2344

    assert len(VR_D2344) == 21
