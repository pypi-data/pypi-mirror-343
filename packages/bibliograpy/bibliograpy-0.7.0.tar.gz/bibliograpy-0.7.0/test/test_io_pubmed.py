"""Test module for Pubmed IO"""
from pathlib import Path
from typing import TextIO

from bibliograpy.api_core import Formats
from bibliograpy.api_mesh import MeshPublicationType
from bibliograpy.api_pubmed import Tags
from bibliograpy.io_pubmed import PubmedInputFormat


def read_entries(i: TextIO):
    """ris entry parsing shortcut"""
    return PubmedInputFormat(Formats.PUBMED).from_standard(i)

def test_sample1():
    """test pubmed sample1"""

    with open(Path(__file__).parent / 'resources' / 'pubmed' / 'sample1.nbib', encoding='utf-8') as s:
        result = read_entries(s)
        assert len(result) == 1
        assert result[0] == {
            Tags.IP: '2',
            Tags.AB: 'Sixty-seven Holstein-Friesian cows, from '
                                     '20\xa0days postpartum, were recruited '
                                     'into the study and fitted with both a '
                                     'pedometer (SAE Afikim) and a Heatime '
                                     'neck collar (SCR Engineers) and '
                                     'allocated a heat mount detector (either '
                                     'scratchcard [Dairymac] or KaMaR [KaMaR]) '
                                     'or left with none, relying only on farm '
                                     'staff observation. Common production '
                                     'stressors and other factors were '
                                     'assessed to determine their impact on '
                                     'the ability of each method to accurately '
                                     'detect oestrus and to investigate '
                                     'effects on the frequency of '
                                     'false-positive detections. Only 74 per '
                                     'cent of all potential oestrus periods '
                                     '(episodes of low progesterone) were '
                                     'identified by combining information from '
                                     'all methods. There was no difference '
                                     'between the methods in terms of '
                                     'sensitivity for detecting ‘true oestrus '
                                     'events’ (approximately 60 per cent), '
                                     'with the exception of scratchcards, '
                                     'which were less efficient (36 per cent). '
                                     'Pedometers and KaMaRs had higher numbers '
                                     'of false-positive identifications. No '
                                     'production stressors had any consequence '
                                     'on false-positives. The positive '
                                     'predictive values for neck collars or '
                                     'observation by farm staff were higher '
                                     'than those of other methods, and '
                                     'combining these two methods yielded the '
                                     'best results. Neck collars did not '
                                     'detect any of the nine oestrus events '
                                     'occurring in three cows with a body '
                                     'condition score (BCS) of less than 2, '
                                     'and the efficiency of correctly '
                                     'identifying oestrus was also reduced by '
                                     'high milk yield (odds ratio [OR]=0.34). '
                                     'Pedometer efficiency was reduced by '
                                     'lameness, low BCS or high milk yield '
                                     '(OR=0.42, 0.15 or 0.30, respectively).',
            Tags.AU: ['Holman, A.',
                      'Thompson, J.',
                      'Routly, J. E.',
                      'Cameron, J.',
                      'Jones, D. N.',
                      'Grove-White, D.',
                      'Smith, R. F.',
                      'Dobson, H.'],
            Tags.PG: '47-47',
            Tags.PMID: '21730035',
            Tags.PT: [MeshPublicationType.JOURNAL_ARTICLE],
            Tags.SO: 'Veterinary Record 2011-07-01 169(2): 47-47',
            Tags.TA: 'Veterinary Record',
            Tags.TI: 'Comparison of oestrus detection methods in dairy cattle',
            Tags.VI: '169',
            Tags.AID: 'https://doi.org/10.1136/vr.d2344 [doi]',
            Tags.DP: '2011'
        }

def test_sample2():
    """test endnote sample2 (extension tags)"""

    with open(Path(__file__).parent / 'resources' / 'pubmed' / 'sample2.nbib', encoding='utf-8') as s:
        result = read_entries(s)
        assert len(result) == 1
        assert result[0] == {
            Tags.IP: '2',
            Tags.AB: 'Sixty-seven Holstein-Friesian cows, from '
                                     '20\xa0days postpartum, were recruited '
                                     'into the study and fitted with both a '
                                     'pedometer (SAE Afikim) and a Heatime '
                                     'neck collar (SCR Engineers) and '
                                     'allocated a heat mount detector (either '
                                     'scratchcard [Dairymac] or KaMaR [KaMaR]) '
                                     'or left with none, relying only on farm '
                                     'staff observation. Common production '
                                     'stressors and other factors were '
                                     'assessed to determine their impact on '
                                     'the ability of each method to accurately '
                                     'detect oestrus and to investigate '
                                     'effects on the frequency of '
                                     'false-positive detections. Only 74 per '
                                     'cent of all potential oestrus periods '
                                     '(episodes of low progesterone) were '
                                     'identified by combining information from '
                                     'all methods. There was no difference '
                                     'between the methods in terms of '
                                     'sensitivity for detecting ‘true oestrus '
                                     'events’ (approximately 60 per cent), '
                                     'with the exception of scratchcards, '
                                     'which were less efficient (36 per cent). '
                                     'Pedometers and KaMaRs had higher numbers '
                                     'of false-positive identifications. No '
                                     'production stressors had any consequence '
                                     'on false-positives. The positive '
                                     'predictive values for neck collars or '
                                     'observation by farm staff were higher '
                                     'than those of other methods, and '
                                     'combining these two methods yielded the '
                                     'best results. Neck collars did not '
                                     'detect any of the nine oestrus events '
                                     'occurring in three cows with a body '
                                     'condition score (BCS) of less than 2, '
                                     'and the efficiency of correctly '
                                     'identifying oestrus was also reduced by '
                                     'high milk yield (odds ratio [OR]=0.34). '
                                     'Pedometer efficiency was reduced by '
                                     'lameness, low BCS or high milk yield '
                                     '(OR=0.42, 0.15 or 0.30, respectively).',
            Tags.AU: ['Holman, A.',
                      'Thompson, J.',
                      'Routly, J. E.',
                      'Cameron, J.',
                      'Jones, D. N.',
                      'Grove-White, D.',
                      'Smith, R. F.',
                      'Dobson, H.'],
            Tags.PG: '47-47',
            Tags.PMID: '21730035',
            Tags.PT: [MeshPublicationType.JOURNAL_ARTICLE],
            Tags.SO: 'Veterinary Record 2011-07-01 169(2): 47-47',
            Tags.TA: 'Veterinary Record',
            Tags.TI: 'Comparison of oestrus detection methods in dairy cattle',
            Tags.VI: '169',
            Tags.AID: 'https://doi.org/10.1136/vr.d2344 [doi]',
            Tags.DP: '2011',
            '4099': 'https://bvajournals.onlinelibrary.wiley.com/doi/abs/10.1136/vr.d2344',
            '4100': 'https://bvajournals.onlinelibrary.wiley.com/doi/full/10.1136/vr.d2344'
        }

def test_sample3():
    """test endnote sample3 (multiple entries)"""


    with open(Path(__file__).parent / 'resources' / 'pubmed' / 'sample3.nbib', encoding='utf-8') as s:
        result = read_entries(s)
        assert len(result) == 2
        assert result[0] == {
            Tags.IP: '2',
            Tags.AB: 'Sixty-seven Holstein-Friesian cows, from '
                                     '20\xa0days postpartum, were recruited '
                                     'into the study and fitted with both a '
                                     'pedometer (SAE Afikim) and a Heatime '
                                     'neck collar (SCR Engineers) and '
                                     'allocated a heat mount detector (either '
                                     'scratchcard [Dairymac] or KaMaR [KaMaR]) '
                                     'or left with none, relying only on farm '
                                     'staff observation. Common production '
                                     'stressors and other factors were '
                                     'assessed to determine their impact on '
                                     'the ability of each method to accurately '
                                     'detect oestrus and to investigate '
                                     'effects on the frequency of '
                                     'false-positive detections. Only 74 per '
                                     'cent of all potential oestrus periods '
                                     '(episodes of low progesterone) were '
                                     'identified by combining information from '
                                     'all methods. There was no difference '
                                     'between the methods in terms of '
                                     'sensitivity for detecting ‘true oestrus '
                                     'events’ (approximately 60 per cent), '
                                     'with the exception of scratchcards, '
                                     'which were less efficient (36 per cent). '
                                     'Pedometers and KaMaRs had higher numbers '
                                     'of false-positive identifications. No '
                                     'production stressors had any consequence '
                                     'on false-positives. The positive '
                                     'predictive values for neck collars or '
                                     'observation by farm staff were higher '
                                     'than those of other methods, and '
                                     'combining these two methods yielded the '
                                     'best results. Neck collars did not '
                                     'detect any of the nine oestrus events '
                                     'occurring in three cows with a body '
                                     'condition score (BCS) of less than 2, '
                                     'and the efficiency of correctly '
                                     'identifying oestrus was also reduced by '
                                     'high milk yield (odds ratio [OR]=0.34). '
                                     'Pedometer efficiency was reduced by '
                                     'lameness, low BCS or high milk yield '
                                     '(OR=0.42, 0.15 or 0.30, respectively).',
            Tags.AU: ['Holman, A.',
                      'Thompson, J.',
                      'Routly, J. E.',
                      'Cameron, J.',
                      'Jones, D. N.',
                      'Grove-White, D.',
                      'Smith, R. F.',
                      'Dobson, H.'],
            Tags.PG: '47-47',
            Tags.PMID: '21730035',
            Tags.PT: [MeshPublicationType.JOURNAL_ARTICLE],
            Tags.SO: 'Veterinary Record 2011-07-01 169(2): 47-47',
            Tags.TA: 'Veterinary Record',
            Tags.TI: 'Comparison of oestrus detection methods in dairy cattle',
            Tags.VI: '169',
            Tags.AID: 'https://doi.org/10.1136/vr.d2344 [doi]',
            Tags.DP: '2011'
        }
        assert result[1] == {
            Tags.IP: '2',
            Tags.AB: 'Sixty-seven Holstein-Friesian cows, from '
                                     '20\xa0days postpartum, were recruited '
                                     'into the study and fitted with both a '
                                     'pedometer (SAE Afikim) and a Heatime '
                                     'neck collar (SCR Engineers) and '
                                     'allocated a heat mount detector (either '
                                     'scratchcard [Dairymac] or KaMaR [KaMaR]) '
                                     'or left with none, relying only on farm '
                                     'staff observation. Common production '
                                     'stressors and other factors were '
                                     'assessed to determine their impact on '
                                     'the ability of each method to accurately '
                                     'detect oestrus and to investigate '
                                     'effects on the frequency of '
                                     'false-positive detections. Only 74 per '
                                     'cent of all potential oestrus periods '
                                     '(episodes of low progesterone) were '
                                     'identified by combining information from '
                                     'all methods. There was no difference '
                                     'between the methods in terms of '
                                     'sensitivity for detecting ‘true oestrus '
                                     'events’ (approximately 60 per cent), '
                                     'with the exception of scratchcards, '
                                     'which were less efficient (36 per cent). '
                                     'Pedometers and KaMaRs had higher numbers '
                                     'of false-positive identifications. No '
                                     'production stressors had any consequence '
                                     'on false-positives. The positive '
                                     'predictive values for neck collars or '
                                     'observation by farm staff were higher '
                                     'than those of other methods, and '
                                     'combining these two methods yielded the '
                                     'best results. Neck collars did not '
                                     'detect any of the nine oestrus events '
                                     'occurring in three cows with a body '
                                     'condition score (BCS) of less than 2, '
                                     'and the efficiency of correctly '
                                     'identifying oestrus was also reduced by '
                                     'high milk yield (odds ratio [OR]=0.34). '
                                     'Pedometer efficiency was reduced by '
                                     'lameness, low BCS or high milk yield '
                                     '(OR=0.42, 0.15 or 0.30, respectively).',
            Tags.AU: ['Holman, A.',
                      'Thompson, J.',
                      'Routly, J. E.',
                      'Cameron, J.',
                      'Jones, D. N.',
                      'Grove-White, D.',
                      'Smith, R. F.',
                      'Dobson, H.'],
            Tags.PG: '47-47',
            Tags.PMID: '21730035',
            Tags.PT: [MeshPublicationType.JOURNAL_ARTICLE],
            Tags.SO: 'Veterinary Record 2011-07-01 169(2): 47-47',
            Tags.TA: 'Veterinary Record',
            Tags.TI: 'Comparison of oestrus detection methods in dairy cattle',
            Tags.VI: '169',
            Tags.AID: 'https://doi.org/10.1136/vr.d2344 [doi]',
            Tags.DP: '2011',
            '4099': 'https://bvajournals.onlinelibrary.wiley.com/doi/abs/10.1136/vr.d2344',
            '4100': 'https://bvajournals.onlinelibrary.wiley.com/doi/full/10.1136/vr.d2344'
        }
