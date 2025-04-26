"""Test module for pubmed process tool."""

from argparse import Namespace
from pathlib import Path
import pydoc
import sys
import time

import yaml

import pytest

from bibliograpy.api_common import cite

from bibliograpy.process import _process


def _ris2001_resource(file: str) -> str:
    """Chemin vers les fichiers d'entrée."""
    return str(Path(Path(__file__).parent / 'resources' / 'pubmed' / file))


def _sibbling_module(file: str) -> str:
    """Chemin vers les fichiers de modules voisins."""
    return str(Path(Path(__file__).parent / file))


def _output(file: str) -> str:
    """Chemin vers les fichiers de sortie."""
    return str(Path(Path(__file__).parent / 'resources' / 'pubmed' / 'out' / file))


def test_pubmed_yml_to_yml():
    """test process from a yml bibliography to a yml bibliography"""

    _process(Namespace(CMD='pubmed',
                       file=_ris2001_resource('sample1.yml'),
                       output_file=_output('test_pubmed_yml_to_yml.yml'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_pubmed_yml_to_yml.yml'), encoding='utf-8') as s:
        content = yaml.safe_load(s)
        assert content == [{'AB': 'Sixty-seven Holstein-Friesian cows, from 20\xa0days postpartum, were '
                                  'recruited into the study and fitted with both a pedometer (SAE '
                                  'Afikim) and a Heatime neck collar (SCR Engineers) and allocated a '
                                  'heat mount detector (either scratchcard [Dairymac] or KaMaR [KaMaR]) '
                                  'or left with none, relying only on farm staff observation. Common '
                                  'production stressors and other factors were assessed to determine '
                                  'their impact on the ability of each method to accurately detect '
                                  'oestrus and to investigate effects on the frequency of false-positive '
                                  'detections. Only 74 per cent of all potential oestrus periods '
                                  '(episodes of low progesterone) were identified by combining '
                                  'information from all methods. There was no difference between the '
                                  'methods in terms of sensitivity for detecting ‘true oestrus events’ '
                                  '(approximately 60 per cent), with the exception of scratchcards, '
                                  'which were less efficient (36 per cent). Pedometers and KaMaRs had '
                                  'higher numbers of false-positive identifications. No production '
                                  'stressors had any consequence on false-positives. The positive '
                                  'predictive values for neck collars or observation by farm staff were '
                                  'higher than those of other methods, and combining these two methods '
                                  'yielded the best results. Neck collars did not detect any of the nine '
                                  'oestrus events occurring in three cows with a body condition score '
                                  '(BCS) of less than 2, and the efficiency of correctly identifying '
                                  'oestrus was also reduced by high milk yield (odds ratio [OR]=0.34). '
                                  'Pedometer efficiency was reduced by lameness, low BCS or high milk '
                                  'yield (OR=0.42, 0.15 or 0.30, respectively).',
                            'AID': 'https://doi.org/10.1136/vr.d2344 [doi]',
                            'AU': ['Holman, A.',
                                   'Thompson, J.',
                                   'Routly, J. E.',
                                   'Cameron, J.',
                                   'Jones, D. N.',
                                   'Grove-White, D.',
                                   'Smith, R. F.',
                                   'Dobson, H.'],
                            'DP': '2011',
                            'IP': '2',
                            'PG': '47-47',
                            'PMID': '21730035',
                            'PT': ['Journal Article'],
                            'SO': 'Veterinary Record 2011-07-01 169(2): 47-47',
                            'TA': 'Veterinary Record',
                            'TI': 'Comparison of oestrus detection methods in dairy cattle',
                            'VI': '169'}]

def test_pubmed_yml_to_pubmed():
    """test process from a yml bibliography to a RIS 2001 bibliography"""

    _process(Namespace(CMD='pubmed',
                       file=_ris2001_resource('sample1.yml'),
                       output_file=_output('test_pubmed_yml_to_pubmed.nbib'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_pubmed_yml_to_pubmed.nbib'), encoding='utf-8') as s:
        content = s.read()
        assert content == """AU  - Holman, A.
AU  - Thompson, J.
AU  - Routly, J. E.
AU  - Cameron, J.
AU  - Jones, D. N.
AU  - Grove-White, D.
AU  - Smith, R. F.
AU  - Dobson, H.
TI  - Comparison of oestrus detection methods in dairy cattle
PT  - Journal Article
DP  - 2011
TA  - Veterinary Record
PG  - 47-47
VI  - 169
IP  - 2
AID - https://doi.org/10.1136/vr.d2344 [doi]
PMID- 21730035
SO  - Veterinary Record 2011-07-01 169(2): 47-47
AB  - Sixty-seven Holstein-Friesian cows, from 20 days postpartum, were recruited into the study and fitted with \
both a pedometer (SAE Afikim) and a Heatime neck collar (SCR Engineers) and allocated a heat mount detector \
(either scratchcard [Dairymac] or KaMaR [KaMaR]) or left with none, relying only on farm staff observation. \
Common production stressors and other factors were assessed to determine their impact on the ability of each \
method to accurately detect oestrus and to investigate effects on the frequency of false-positive detections. \
Only 74 per cent of all potential oestrus periods (episodes of low progesterone) were identified by combining \
information from all methods. There was no difference between the methods in terms of sensitivity for detecting \
‘true oestrus events’ (approximately 60 per cent), with the exception of scratchcards, which were less efficient \
(36 per cent). Pedometers and KaMaRs had higher numbers of false-positive identifications. No production stressors \
had any consequence on false-positives. The positive predictive values for neck collars or observation by farm staff \
were higher than those of other methods, and combining these two methods yielded the best results. Neck collars \
did not detect any of the nine oestrus events occurring in three cows with a body condition score (BCS) of less \
than 2, and the efficiency of correctly identifying oestrus was also reduced by high milk yield \
(odds ratio [OR]=0.34). Pedometer efficiency was reduced by lameness, low BCS or high milk yield \
(OR=0.42, 0.15 or 0.30, respectively).
"""

def test_pubmed_yml_to_json():
    """test process from a yml bibliography to a RIS 2001 bibliography"""

    _process(Namespace(CMD='pubmed',
                       file=_ris2001_resource('sample1.yml'),
                       output_file=_output('test_pubmed_yml_to_json.json'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_pubmed_yml_to_json.json'), encoding='utf-8') as s:
        content = s.read()

        assert content == ('[{"AU": ["Holman, A.", "Thompson, J.", "Routly, J. E.", "Cameron, J.", "Jones, D. N.", '
                           '"Grove-White, D.", "Smith, R. F.", "Dobson, H."], '
                           '"TI": "Comparison of oestrus detection methods in dairy cattle", '
                           '"PT": ["Journal Article"], '
                           '"DP": "2011", '
                           '"TA": "Veterinary Record", '
                           '"PG": "47-47", '
                           '"VI": "169", '
                           '"IP": "2", '
                           '"AID": "https://doi.org/10.1136/vr.d2344 [doi]", '
                           '"PMID": "21730035", '
                           '"SO": "Veterinary Record 2011-07-01 169(2): 47-47", '
                           '"AB": "Sixty-seven Holstein-Friesian cows, from 20\\u00a0days postpartum, '
                           'were recruited into the study and fitted with both a pedometer (SAE Afikim) '
                           'and a Heatime neck collar (SCR Engineers) and allocated a heat mount detector '
                           '(either scratchcard [Dairymac] or KaMaR [KaMaR]) or left with none, relying only on farm '
                           'staff observation. Common production stressors and other factors were assessed to '
                           'determine their impact on the ability of each method to accurately detect oestrus '
                           'and to investigate effects on the frequency of false-positive detections. Only 74 per '
                           'cent of all potential oestrus periods (episodes of low progesterone) were identified by '
                           'combining information from all methods. There was no difference between the methods in '
                           'terms of sensitivity for detecting \\u2018true oestrus events\\u2019 (approximately 60 per '
                           'cent), with the exception of scratchcards, which were less efficient (36 per cent). '
                           'Pedometers and KaMaRs had higher numbers of false-positive identifications. No production '
                           'stressors had any consequence on false-positives. The positive predictive values for neck '
                           'collars or observation by farm staff were higher than those of other methods, and '
                           'combining these two methods yielded the best results. Neck collars did not detect any of '
                           'the nine oestrus events occurring in three cows with a body condition score (BCS) of '
                           'less than 2, and the efficiency of correctly identifying oestrus was also reduced by high '
                           'milk yield (odds ratio [OR]=0.34). Pedometer efficiency was reduced by lameness, low BCS '
                           'or high milk yield (OR=0.42, 0.15 or 0.30, respectively)."}]')

def test_pubmed_json_to_yml():
    """test process from a json bibliography to a yml bibliography"""

    _process(Namespace(CMD='pubmed',
                       file=_ris2001_resource('sample1.json'),
                       output_file=_output('test_pubmed_json_to_yml.yml'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_pubmed_json_to_yml.yml'), encoding='utf-8') as s:
        content = yaml.safe_load(s)

        assert content == [{'AB': 'Sixty-seven Holstein-Friesian cows, from 20\xa0days postpartum, were '
                                  'recruited into the study and fitted with both a pedometer (SAE '
                                  'Afikim) and a Heatime neck collar (SCR Engineers) and allocated a '
                                  'heat mount detector (either scratchcard [Dairymac] or KaMaR [KaMaR]) '
                                  'or left with none, relying only on farm staff observation. Common '
                                  'production stressors and other factors were assessed to determine '
                                  'their impact on the ability of each method to accurately detect '
                                  'oestrus and to investigate effects on the frequency of false-positive '
                                  'detections. Only 74 per cent of all potential oestrus periods '
                                  '(episodes of low progesterone) were identified by combining '
                                  'information from all methods. There was no difference between the '
                                  'methods in terms of sensitivity for detecting ‘true oestrus events’ '
                                  '(approximately 60 per cent), with the exception of scratchcards, '
                                  'which were less efficient (36 per cent). Pedometers and KaMaRs had '
                                  'higher numbers of false-positive identifications. No production '
                                  'stressors had any consequence on false-positives. The positive '
                                  'predictive values for neck collars or observation by farm staff were '
                                  'higher than those of other methods, and combining these two methods '
                                  'yielded the best results. Neck collars did not detect any of the nine '
                                  'oestrus events occurring in three cows with a body condition score '
                                  '(BCS) of less than 2, and the efficiency of correctly identifying '
                                  'oestrus was also reduced by high milk yield (odds ratio [OR]=0.34). '
                                  'Pedometer efficiency was reduced by lameness, low BCS or high milk '
                                  'yield (OR=0.42, 0.15 or 0.30, respectively).',
                            'AID': 'https://doi.org/10.1136/vr.d2344 [doi]',
                            'AU': ['Holman, A.',
                                   'Thompson, J.',
                                   'Routly, J. E.',
                                   'Cameron, J.',
                                   'Jones, D. N.',
                                   'Grove-White, D.',
                                   'Smith, R. F.',
                                   'Dobson, H.'],
                            'DP': '2011',
                            'IP': '2',
                            'PG': '47-47',
                            'PMID': '21730035',
                            'PT': ['Journal Article'],
                            'SO': 'Veterinary Record 2011-07-01 169(2): 47-47',
                            'TA': 'Veterinary Record',
                            'TI': 'Comparison of oestrus detection methods in dairy cattle',
                            'VI': '169'}]

def test_pubmed_json_to_pubmed():
    """test process from a json bibliography to a RIS 2001 bibliography"""

    _process(Namespace(CMD='pubmed',
                       file=_ris2001_resource('sample1.json'),
                       output_file=_output('test_pubmed_json_to_pubmed.nbib'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_pubmed_json_to_pubmed.nbib'), encoding='utf-8') as s:
        content = s.read()
        assert content == """AU  - Holman, A.
AU  - Thompson, J.
AU  - Routly, J. E.
AU  - Cameron, J.
AU  - Jones, D. N.
AU  - Grove-White, D.
AU  - Smith, R. F.
AU  - Dobson, H.
TI  - Comparison of oestrus detection methods in dairy cattle
PT  - Journal Article
DP  - 2011
TA  - Veterinary Record
PG  - 47-47
VI  - 169
IP  - 2
AID - https://doi.org/10.1136/vr.d2344 [doi]
PMID- 21730035
SO  - Veterinary Record 2011-07-01 169(2): 47-47
AB  - Sixty-seven Holstein-Friesian cows, from 20 days postpartum, were recruited into the study and fitted with \
both a pedometer (SAE Afikim) and a Heatime neck collar (SCR Engineers) and allocated a heat mount detector \
(either scratchcard [Dairymac] or KaMaR [KaMaR]) or left with none, relying only on farm staff observation. \
Common production stressors and other factors were assessed to determine their impact on the ability of each \
method to accurately detect oestrus and to investigate effects on the frequency of false-positive detections. \
Only 74 per cent of all potential oestrus periods (episodes of low progesterone) were identified by combining \
information from all methods. There was no difference between the methods in terms of sensitivity for detecting \
‘true oestrus events’ (approximately 60 per cent), with the exception of scratchcards, which were less efficient \
(36 per cent). Pedometers and KaMaRs had higher numbers of false-positive identifications. No production stressors \
had any consequence on false-positives. The positive predictive values for neck collars or observation by farm staff \
were higher than those of other methods, and combining these two methods yielded the best results. Neck collars \
did not detect any of the nine oestrus events occurring in three cows with a body condition score (BCS) of less \
than 2, and the efficiency of correctly identifying oestrus was also reduced by high milk yield \
(odds ratio [OR]=0.34). Pedometer efficiency was reduced by lameness, low BCS or high milk yield \
(OR=0.42, 0.15 or 0.30, respectively).
"""

def test_pubmed_json_to_json():
    """test process from a json bibliography to a json bibliography"""

    _process(Namespace(CMD='pubmed',
                       file=_ris2001_resource('sample1.json'),
                       output_file=_output('test_pubmed_json_to_json.json'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_pubmed_json_to_json.json'), encoding='utf-8') as s:
        content = s.read()

        assert content == ('[{"AU": ["Holman, A.", "Thompson, J.", "Routly, J. E.", "Cameron, J.", "Jones, D. N.", '
                           '"Grove-White, D.", "Smith, R. F.", "Dobson, H."], '
                           '"TI": "Comparison of oestrus detection methods in dairy cattle", '
                           '"PT": ["Journal Article"], '
                           '"DP": "2011", '
                           '"TA": "Veterinary Record", '
                           '"PG": "47-47", '
                           '"VI": "169", '
                           '"IP": "2", '
                           '"AID": "https://doi.org/10.1136/vr.d2344 [doi]", '
                           '"PMID": "21730035", '
                           '"SO": "Veterinary Record 2011-07-01 169(2): 47-47", '
                           '"AB": "Sixty-seven Holstein-Friesian cows, from 20\\u00a0days postpartum, '
                           'were recruited into the study and fitted with both a pedometer (SAE Afikim) '
                           'and a Heatime neck collar (SCR Engineers) and allocated a heat mount detector '
                           '(either scratchcard [Dairymac] or KaMaR [KaMaR]) or left with none, relying only on farm '
                           'staff observation. Common production stressors and other factors were assessed to '
                           'determine their impact on the ability of each method to accurately detect oestrus '
                           'and to investigate effects on the frequency of false-positive detections. Only 74 per '
                           'cent of all potential oestrus periods (episodes of low progesterone) were identified by '
                           'combining information from all methods. There was no difference between the methods in '
                           'terms of sensitivity for detecting \\u2018true oestrus events\\u2019 (approximately 60 per '
                           'cent), with the exception of scratchcards, which were less efficient (36 per cent). '
                           'Pedometers and KaMaRs had higher numbers of false-positive identifications. No production '
                           'stressors had any consequence on false-positives. The positive predictive values for neck '
                           'collars or observation by farm staff were higher than those of other methods, and '
                           'combining these two methods yielded the best results. Neck collars did not detect any of '
                           'the nine oestrus events occurring in three cows with a body condition score (BCS) of '
                           'less than 2, and the efficiency of correctly identifying oestrus was also reduced by high '
                           'milk yield (odds ratio [OR]=0.34). Pedometer efficiency was reduced by lameness, low BCS '
                           'or high milk yield (OR=0.42, 0.15 or 0.30, respectively)."}]')

def test_pubmed_pubmed_to_yml():
    """test process from a bib bibliography to a yml bibliography"""

    _process(Namespace(CMD='pubmed',
                       file=_ris2001_resource('sample1.nbib'),
                       output_file=_output('test_pubmed_pubmed_to_yml.yml'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_pubmed_pubmed_to_yml.yml'), encoding='utf-8') as s:
        content = yaml.safe_load(s)
        assert content == [{'AB': 'Sixty-seven Holstein-Friesian cows, from 20\xa0days postpartum, were '
        'recruited into the study and fitted with both a pedometer (SAE '
        'Afikim) and a Heatime neck collar (SCR Engineers) and allocated a '
        'heat mount detector (either scratchcard [Dairymac] or KaMaR [KaMaR]) '
        'or left with none, relying only on farm staff observation. Common '
        'production stressors and other factors were assessed to determine '
        'their impact on the ability of each method to accurately detect '
        'oestrus and to investigate effects on the frequency of false-positive '
        'detections. Only 74 per cent of all potential oestrus periods '
        '(episodes of low progesterone) were identified by combining '
        'information from all methods. There was no difference between the '
        'methods in terms of sensitivity for detecting ‘true oestrus events’ '
        '(approximately 60 per cent), with the exception of scratchcards, '
        'which were less efficient (36 per cent). Pedometers and KaMaRs had '
        'higher numbers of false-positive identifications. No production '
        'stressors had any consequence on false-positives. The positive '
        'predictive values for neck collars or observation by farm staff were '
        'higher than those of other methods, and combining these two methods '
        'yielded the best results. Neck collars did not detect any of the nine '
        'oestrus events occurring in three cows with a body condition score '
        '(BCS) of less than 2, and the efficiency of correctly identifying '
        'oestrus was also reduced by high milk yield (odds ratio [OR]=0.34). '
        'Pedometer efficiency was reduced by lameness, low BCS or high milk '
        'yield (OR=0.42, 0.15 or 0.30, respectively).',
  'AID': 'https://doi.org/10.1136/vr.d2344 [doi]',
  'AU': ['Holman, A.',
         'Thompson, J.',
         'Routly, J. E.',
         'Cameron, J.',
         'Jones, D. N.',
         'Grove-White, D.',
         'Smith, R. F.',
         'Dobson, H.'],
  'DP': '2011',
  'IP': '2',
  'PG': '47-47',
  'PMID': '21730035',
  'PT': ['Journal Article'],
  'SO': 'Veterinary Record 2011-07-01 169(2): 47-47',
  'TA': 'Veterinary Record',
  'TI': 'Comparison of oestrus detection methods in dairy cattle',
  'VI': '169'}]

def test_pubmed_pubmed_to_pubmed():
    """test process from a RIS 2001 bibliography to a RIS 2001 bibliography"""

    _process(Namespace(CMD='pubmed',
                       file=_ris2001_resource('sample1.nbib'),
                       output_file=_output('test_pubmed_pubmed_to_pubmed.nbib'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_pubmed_pubmed_to_pubmed.nbib'), encoding='utf-8') as s:
        content = s.read()
        assert content == """AU  - Holman, A.
AU  - Thompson, J.
AU  - Routly, J. E.
AU  - Cameron, J.
AU  - Jones, D. N.
AU  - Grove-White, D.
AU  - Smith, R. F.
AU  - Dobson, H.
TI  - Comparison of oestrus detection methods in dairy cattle
PT  - Journal Article
DP  - 2011
TA  - Veterinary Record
PG  - 47-47
VI  - 169
IP  - 2
AID - https://doi.org/10.1136/vr.d2344 [doi]
PMID- 21730035
SO  - Veterinary Record 2011-07-01 169(2): 47-47
AB  - Sixty-seven Holstein-Friesian cows, from 20 days postpartum, were recruited into the study and fitted with \
both a pedometer (SAE Afikim) and a Heatime neck collar (SCR Engineers) and allocated a heat mount detector \
(either scratchcard [Dairymac] or KaMaR [KaMaR]) or left with none, relying only on farm staff observation. \
Common production stressors and other factors were assessed to determine their impact on the ability of each \
method to accurately detect oestrus and to investigate effects on the frequency of false-positive detections. \
Only 74 per cent of all potential oestrus periods (episodes of low progesterone) were identified by combining \
information from all methods. There was no difference between the methods in terms of sensitivity for detecting \
‘true oestrus events’ (approximately 60 per cent), with the exception of scratchcards, which were less efficient \
(36 per cent). Pedometers and KaMaRs had higher numbers of false-positive identifications. No production stressors \
had any consequence on false-positives. The positive predictive values for neck collars or observation by farm staff \
were higher than those of other methods, and combining these two methods yielded the best results. Neck collars \
did not detect any of the nine oestrus events occurring in three cows with a body condition score (BCS) of less \
than 2, and the efficiency of correctly identifying oestrus was also reduced by high milk yield \
(odds ratio [OR]=0.34). Pedometer efficiency was reduced by lameness, low BCS or high milk yield \
(OR=0.42, 0.15 or 0.30, respectively).
"""

def test_pubmed_pubmed_to_json():
    """test process from a RIS 2001 bibliography to a json bibliography"""

    _process(Namespace(CMD='pubmed',
                       file=_ris2001_resource('sample1.nbib'),
                       output_file=_output('test_pubmed_pubmed_to_json.json'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_pubmed_pubmed_to_json.json'), encoding='utf-8') as s:
        content = s.read()
        assert content == ('[{"AU": ["Holman, A.", "Thompson, J.", "Routly, J. E.", "Cameron, J.", "Jones, D. N.", '
                           '"Grove-White, D.", "Smith, R. F.", "Dobson, H."], '
                           '"TI": "Comparison of oestrus detection methods in dairy cattle", '
                           '"PT": ["Journal Article"], '
                           '"DP": "2011", '
                           '"TA": "Veterinary Record", '
                           '"PG": "47-47", '
                           '"VI": "169", '
                           '"IP": "2", '
                           '"AID": "https://doi.org/10.1136/vr.d2344 [doi]", '
                           '"PMID": "21730035", '
                           '"SO": "Veterinary Record 2011-07-01 169(2): 47-47", '
                           '"AB": "Sixty-seven Holstein-Friesian cows, from 20\\u00a0days postpartum, '
                           'were recruited into the study and fitted with both a pedometer (SAE Afikim) '
                           'and a Heatime neck collar (SCR Engineers) and allocated a heat mount detector '
                           '(either scratchcard [Dairymac] or KaMaR [KaMaR]) or left with none, relying only on farm '
                           'staff observation. Common production stressors and other factors were assessed to '
                           'determine their impact on the ability of each method to accurately detect oestrus '
                           'and to investigate effects on the frequency of false-positive detections. Only 74 per '
                           'cent of all potential oestrus periods (episodes of low progesterone) were identified by '
                           'combining information from all methods. There was no difference between the methods in '
                           'terms of sensitivity for detecting \\u2018true oestrus events\\u2019 (approximately 60 per '
                           'cent), with the exception of scratchcards, which were less efficient (36 per cent). '
                           'Pedometers and KaMaRs had higher numbers of false-positive identifications. No production '
                           'stressors had any consequence on false-positives. The positive predictive values for neck '
                           'collars or observation by farm staff were higher than those of other methods, and '
                           'combining these two methods yielded the best results. Neck collars did not detect any of '
                           'the nine oestrus events occurring in three cows with a body condition score (BCS) of '
                           'less than 2, and the efficiency of correctly identifying oestrus was also reduced by high '
                           'milk yield (odds ratio [OR]=0.34). Pedometer efficiency was reduced by lameness, low BCS '
                           'or high milk yield (OR=0.42, 0.15 or 0.30, respectively)."}]')

def test_pubmed_yml_to_py():
    """test process from a yml bibliography to a py source bibliography"""

    _process(Namespace(CMD='pubmed',
                       file=_ris2001_resource('mini.yml'),
                       output_file=_sibbling_module('test_pubmed_yml_to_py.py'),
                       encoding='utf-8',
                       output_dir='.'))

    time.sleep(1) # wait for the bibliography source file to be generated

    from test_pubmed_yml_to_py import IAU, NASA

    @cite(IAU, NASA)
    def bib_ref_foo():
        """ma doc avec plusieurs références en varargs"""

    if sys.version_info.minor >= 12:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_process_pubmed

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références en varargs

    Bibliography:

    * International Astronomical Union [iau]
    * NASA [nasa]
""")
    else:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_process_pubmed

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références en varargs
    
    Bibliography:
    
    * International Astronomical Union [iau]
    * NASA [nasa]
""")

def test_pubmed_json_to_py():
    """test process from a yml bibliography to a py source bibliography"""

    _process(Namespace(CMD='pubmed',
                       file=_ris2001_resource('mini.json'),
                       output_file=_sibbling_module('test_pubmed_json_to_py.py'),
                       encoding='utf-8',
                       output_dir='.'))

    time.sleep(1) # wait for the bibliography source file to be generated

    from test_pubmed_json_to_py import IAU, NASA

    @cite(IAU, NASA)
    def bib_ref_foo():
        """ma doc avec plusieurs références en varargs"""

    if sys.version_info.minor >= 12:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_process_pubmed

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références en varargs

    Bibliography:

    * International Astronomical Union [iau]
    * NASA [nasa]
""")
    else:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_process_pubmed

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références en varargs
    
    Bibliography:
    
    * International Astronomical Union [iau]
    * NASA [nasa]
""")

def test_pubmed_pubmed_to_py():
    """test process from a yml bibliography to a py source bibliography"""

    _process(Namespace(CMD='pubmed',
                       file=_ris2001_resource('mini.nbib'),
                       output_file=_sibbling_module('test_pubmed_pubmed_to_py.py'),
                       encoding='utf-8',
                       output_dir='.'))

    time.sleep(1) # wait for the bibliography source file to be generated

    from test_pubmed_pubmed_to_py import IAU, NASA

    @cite(IAU, NASA)
    def bib_ref_foo():
        """ma doc avec plusieurs références en varargs"""

    if sys.version_info.minor >= 12:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_process_pubmed

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références en varargs

    Bibliography:

    * International Astronomical Union [iau]
    * NASA [nasa]
""")
    else:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_process_pubmed

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références en varargs
    
    Bibliography:
    
    * International Astronomical Union [iau]
    * NASA [nasa]
""")

def test_input_file_not_found():
    """test process input file not found"""

    with pytest.raises(FileNotFoundError) as e:
        with open(_ris2001_resource('not_existing_file.yml'), encoding='utf-8') as s:
            yaml.safe_load(s)

    assert e.value.args[0] == 2
    assert e.value.args[1] == "No such file or directory"
