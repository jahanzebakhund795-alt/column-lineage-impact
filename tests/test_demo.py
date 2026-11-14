import copy
import json
from pathlib import Path
import unittest
from main import run


class DemoTests(unittest.TestCase):
    def test_business_result(self):
        data = json.loads(Path('sample.json').read_text())
        original = copy.deepcopy(data)
        result = run(data)
        self.assertEqual(len(result['impacted']),3)
        self.assertIn('dashboard.revenue',result['impacted'])
        self.assertEqual(data, original, 'Input should not be mutated')

    def test_boundary_and_failure_behavior(self):
        data = json.loads(Path('sample.json').read_text())
        self.assertEqual(run({'edges':[],'changed':'unknown'})['impacted'], [])
        data['edges'].append(['dashboard.revenue','raw.orders.amount'])
        with self.assertRaises(ValueError):
            run(data)


if __name__ == '__main__':
    unittest.main()
