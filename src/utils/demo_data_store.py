import os
import json
from utils.data_store import DictDataStore

def main():
    # Create a sample JSON file for testing
    test_file = 'temp/data.yaml'
    sample_data = {
        'foo': 'bar',
        'baz': [1, 2, 3],
        'nested': {'a': 1, 'b': 2}
    }
    os.makedirs('temp', exist_ok=True)
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, indent=2)

    # Initialize JsonDataStore
    store = DictDataStore(test_file)

    # Test get
    print('Get foo:', store.get('foo'))
    print('Get baz:', store.get('baz'))
    print('Get nested:', store.get('nested'))

    # Test set
    store.set('new_key', {'x': 42})
    print('After set new_key:', store.get('new_key'))

    # Test delete
    store.delete('foo')
    print('After delete foo:', store.get('foo'))

    # Test all
    print('All data:', store.all())

if __name__ == '__main__':
    main()
