"""Test module for PubMed api"""
from bibliograpy.api_pubmed import Tags

def test_pubmed_support():
    """Test PubMed tag parsing."""
    assert Tags.parse("AID") == Tags.AID
