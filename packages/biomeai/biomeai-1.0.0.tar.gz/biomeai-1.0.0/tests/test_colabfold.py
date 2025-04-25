import pytest
from biomeai import ColabFoldMSA
import os

def test_colabfold_initialization():
    """Test ColabFoldMSA initialization with API key"""
    api_key = "test-key"
    msa = ColabFoldMSA(api_key=api_key)
    assert msa.api_key == api_key

def test_colabfold_initialization_from_env():
    """Test ColabFoldMSA initialization from environment variable"""
    os.environ["NVCF_RUN_KEY"] = "env-test-key"
    msa = ColabFoldMSA()
    assert msa.api_key == "env-test-key"
    del os.environ["NVCF_RUN_KEY"]

def test_colabfold_initialization_error():
    """Test ColabFoldMSA initialization with no API key"""
    if "NVCF_RUN_KEY" in os.environ:
        del os.environ["NVCF_RUN_KEY"]
    with pytest.raises(ValueError):
        ColabFoldMSA()

@pytest.mark.asyncio
async def test_search_input_validation():
    """Test input validation for search method"""
    msa = ColabFoldMSA(api_key="test-key")
    
    # Test with valid sequence
    sequence = "MVPSAGQLALFALGIVLAACQALENSTSPLSADPPVAAAVVSHFNDCPDSHTQFCFHGTCRFL"
    data = await msa._prepare_search_data(
        sequence=sequence,
        e_value=0.0001,
        iterations=1,
        databases=["Uniref30_2302"],
        output_formats=["a3m", "fasta"]
    )
    
    assert data["sequence"] == sequence
    assert data["e_value"] == 0.0001
    assert data["iterations"] == 1
    assert data["databases"] == ["Uniref30_2302"]
    assert data["output_alignment_formats"] == ["a3m", "fasta"]

@pytest.mark.integration
def test_full_search_sync():
    """Integration test for synchronous search (requires valid API key)"""
    api_key = os.getenv("NVCF_RUN_KEY")
    if not api_key:
        pytest.skip("NVCF_RUN_KEY not set")
    
    msa = ColabFoldMSA(api_key=api_key)
    sequence = "MVPSAGQLALFALGIVLAACQALENSTSPLSADPPVAAAVVSHFNDCPDSHTQFCFHGTCRFL"
    
    results = msa.search_sync(sequence=sequence)
    assert results is not None
    assert "alignments" in results
