import argparse
from utils.data_store import DictDataStore
import os

def combine_catalog_ssp(catalog_data: dict, ssp_data: dict) -> dict:
    """
    Combine catalog and SSP data.
    This is a placeholder for your actual logic.
    """
    # Example: merge ssp_data into catalog_data under a new key
    combined = catalog_data.copy()
    combined['ssp'] = ssp_data
    return combined

def main():
    parser = argparse.ArgumentParser(description='Process OSCAL catalog and SSP, output combined YAML.')
    parser.add_argument('--catalog', required=True, help='Input catalog file (JSON or YAML)')
    parser.add_argument('--ssp', required=True, help='Input SSP file (JSON or YAML)')
    parser.add_argument('--output', required=True, help='Output YAML file')
    args = parser.parse_args()

    # Load input files
    catalog_store = DictDataStore(args.catalog)
    ssp_store = DictDataStore(args.ssp)

    # Combine data
    combined_data = combine_catalog_ssp(catalog_store.all(), ssp_store.all())

    # Save to output YAML
    # Force output as YAML
    import yaml
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        yaml.safe_dump(combined_data, f, default_flow_style=False, allow_unicode=True)
    print(f'Combined data written to {args.output}')

if __name__ == '__main__':
    main()
