"""Test module for Mesh api"""
from bibliograpy.api_mesh import MeshPublicationType

def test_mesh_type_support():
    """Test PubMed type parsing."""
    assert (MeshPublicationType.parse("Research Support, U.S. Gov't, P.H.S.")
            == MeshPublicationType.RESEARCH_SUPPORT_US_GOVT_PHS)
