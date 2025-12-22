"""
Test database query with sample specifications
"""
from database_mysql import Database
import json

db = Database()

# Test with different specification formats
test_cases = [
    {
        'name': 'Test 1: With mm suffix',
        'specs': {
            'Num of Layers': '2',
            'Thickness': '1.6mm',
            'Track / Spacing': '6/6 mil',
            'Via Hole/Pad': '12/24 mil'
        }
    },
    {
        'name': 'Test 2: Without mm suffix',
        'specs': {
            'Num of Layers': '2',
            'Thickness': '1.6',
            'Track / Spacing': '6 / 6 mil',
            'Via Hole/Pad': '12 / 24 mil'
        }
    },
    {
        'name': 'Test 3: Below thickness',
        'specs': {
            'Num of Layers': '2',
            'Thickness': 'below 0.8',
            'Track / Spacing': '8 / 8 mil',
            'Via Hole/Pad': '12 / 24 mil'
        }
    }
]

for test in test_cases:
    print(f"\n{test['name']}:")
    print(f"Specifications: {test['specs']}")
    try:
        results = db.get_vendor_rates(test['specs'])
        print(f"Found {len(results)} results")
        if results:
            for i, r in enumerate(results[:3], 1):
                print(f"  {i}. {r['vendor_name']}: ${r['rate']:.2f}")
        else:
            print("  No results found")
    except Exception as e:
        print(f"  Error: {e}")

