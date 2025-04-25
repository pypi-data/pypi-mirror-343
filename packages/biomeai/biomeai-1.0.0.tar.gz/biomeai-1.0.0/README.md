# BiomeAI

Simple Python package for Multiple Sequence Alignment search using NVIDIA's ColabFold.

## Install
```bash
pip install biomeai
```

## Quick Usage

```python
from biomeai import ColabFoldMSA

# Initialize with API key
msa = ColabFoldMSA(api_key="your-api-key")
# Or set NVCF_RUN_KEY environment variable

# Your protein sequence
sequence = "MVPSAGQLALFALGIVLAACQALENSTSPLSADPPVAAAVVSHFNDCPDSHTQFCFHGTCRFL"

# 1. Use a single database
results = msa.search_sync(
    sequence=sequence,
    databases=["Uniref30_2302"]
)

# 2. Use multiple databases
results = msa.search_sync(
    sequence=sequence,
    databases=["Uniref30_2302", "PDB70_220313"]
)

# 3. Use all databases (Cascaded Search)
results = msa.search_sync(
    sequence=sequence,
    databases=["Uniref30_2302", "PDB70_220313", "colabfold_envdb_202108"]
)

# Save results (optional)
msa.save_results(results, "results.json")
```

## Available Databases

- `Uniref30_2302`: Universal Reference Database
- `PDB70_220313`: Protein Data Bank
- `colabfold_envdb_202108`: Environmental Database

## Additional Options

```python
results = msa.search_sync(
    sequence=sequence,
    databases=["Uniref30_2302"],
    e_value=0.0001,        # E-value threshold
    iterations=1,          # Number of iterations
    output_formats=["a3m", "fasta"]  # Output formats
)
```

## Async Support

```python
import asyncio

async def search_msa():
    results = await msa.search(
        sequence=sequence,
        databases=["Uniref30_2302"]
    )
    return results

results = asyncio.run(search_msa())
```

## Development

Install with development dependencies:
```bash
pip install biomeai[dev]
```

Run tests:
```bash
pytest
```

## License

MIT License - see the [LICENSE](LICENSE) file for details.
