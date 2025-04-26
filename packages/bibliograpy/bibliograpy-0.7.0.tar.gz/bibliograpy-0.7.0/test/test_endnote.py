"""Test module for endnote."""

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

    _process(Namespace(CMD='endnote',
                       file=_resource('360680.360684.enw'),
                       output_file=_sibbling_module('test_endnote_to_py.py'),
                       encoding='utf-8',
                       output_dir='.'))

    time.sleep(1) # wait for the bibliography source file to be generated

    from test_endnote_to_py import BRIAN_W_KERNIGHANLORINDA_L_CHERRY_1975

    assert len(BRIAN_W_KERNIGHANLORINDA_L_CHERRY_1975) == 13

def test_issue_to_py():
    """test process from a yml bibliography to a py source bibliography"""

    _process(Namespace(CMD='endnote',
                       file=_resource('com_acm_issue.enw'),
                       output_file=_sibbling_module('test_endnote_issue_to_py.py'),
                       encoding='utf-8',
                       output_dir='.'))

    time.sleep(1) # wait for the bibliography source file to be generated

    from test_endnote_issue_to_py import COMMUN_ACM

    assert len(COMMUN_ACM) == 8

def test_example_to_py():
    """test process from a yml bibliography to a py source bibliography"""

    _process(Namespace(CMD='endnote',
                       file=_resource('example.enw'),
                       output_file=_sibbling_module('test_endnote_example_to_py.py'),
                       encoding='utf-8',
                       output_dir='.'))

    time.sleep(1) # wait for the bibliography source file to be generated

    from test_endnote_example_to_py import HOLMAN_ATHOMPSON_JROUTLY_J_E
    from test_endnote_example_to_py import COMPARISON_OF_OESTRUS_DETECTION_METHODS_IN_DAIRY_CATTLE

    assert len(HOLMAN_ATHOMPSON_JROUTLY_J_E) == 2
    assert len(COMPARISON_OF_OESTRUS_DETECTION_METHODS_IN_DAIRY_CATTLE) == 10
