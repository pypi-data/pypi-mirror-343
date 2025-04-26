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

    _process(Namespace(CMD='pubmed',
                       file=_resource('16596158.nbib'),
                       output_file=_sibbling_module('test_pubmed_to_py.py'),
                       encoding='utf-8',
                       output_dir='.'))

    time.sleep(1) # wait for the bibliography source file to be generated

    from test_pubmed_to_py import PUBMED_16596158

    assert len(PUBMED_16596158) == 31


def test_to_py_bis():
    """test process from a yml bibliography to a py source bibliography"""

    _process(Namespace(CMD='pubmed',
                       file=_resource('16596158_bis.nbib'),
                       output_file=_sibbling_module('test_pubmed_bis_to_py.py'),
                       encoding='utf-8',
                       output_dir='.'))

    time.sleep(1) # wait for the bibliography source file to be generated

    from test_pubmed_bis_to_py import PUBMED_16596158, BIS_16596158

    assert len(PUBMED_16596158) == 31
    assert len(BIS_16596158) == 31
