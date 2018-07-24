## -*- coding: utf-8 -*-
import unittest
from actions import apply_all, command_parser
from commands import set_action, get_action, unset_action, counts_action

class TestDB(unittest.TestCase):
    def test_apply(self):
        transactions = [
            [
                {'a': '11'},
                {'b': '22'}
            ],
            [
                {'a': 'DEL VARIABLE'},
                {'b': '33'}
            ]
        ]
        self.assertEqual(apply_all(transactions, {}), {'b': '33'})

    def test_set(self):
        self.assertEqual(set_action(['b', '33'], {}), {'b': '33'})
        self.assertEqual(set_action(['b'], {}), {'b': 'NULL'})

    def test_get(self):
        self.assertEqual(get_action('b', {'b': '33'}), '33')
        self.assertEqual(get_action('c', {'b': '33'}), 'NULL')

    def test_unset(self):
        self.assertEqual(unset_action('b', {'b': '33'}), ({}, None))
        self.assertEqual(unset_action('c', {'b': '33'}), ({'b': '33'}, None))
        self.assertEqual(unset_action('b', {'b': '33'}, {}), ({'b': '33'}, {'b': 'DEL VARIABLE'}))
        self.assertEqual(unset_action('c', {'b': '33'}, {}), ({'b': '33'}, {}))

    def test_counts(self):
        self.assertEqual(counts_action('b', {'b': '33'}), 0)
        self.assertEqual(counts_action('33', {'b': '33', '2': '33'}), 2)

    def test_commands(self):
        DB = {
            "data": {},
            "transactions": []
        }
        _, DB, _ = command_parser('SET a 1', DB)
        self.assertEqual(DB, {"data": {'a': '1'}, "transactions": []})
        _, DB, _ = command_parser('SET a 2', DB)
        self.assertEqual(DB, {"data": {'a': '2'}, "transactions": []})
        _, DB, _ = command_parser('BEGIN', DB)
        self.assertEqual(DB, {"data": {'a': '2'}, "transactions": [[]]})
        _, DB, _ = command_parser('SET b 2', DB)
        self.assertEqual(DB, {"data": {'a': '2'}, "transactions": [[{'b': '2'}]]})
        _, DB, counter = command_parser('COUNTS 2', DB)
        self.assertEqual(counter, 2)
        _, DB, _ = command_parser('BEGIN', DB)
        self.assertEqual(DB, {"data": {'a': '2'}, "transactions": [[{'b': '2'}], []]})
        _, DB, _ = command_parser('UNSET a', DB)
        self.assertEqual(DB, {"data": {'a': '2'}, "transactions": [[{'b': '2'}], [{'a': 'DEL VARIABLE'}]]})
        _, DB, value = command_parser('GET a', DB)
        self.assertEqual(value, 'NULL')
        _, DB, _ = command_parser('ROLLBACK', DB)
        self.assertEqual(DB, {"data": {'a': '2'}, "transactions": [[{'b': '2'}]]})
        _, DB, value = command_parser('GET a', DB)
        self.assertEqual(value, '2')
        _, DB, value = command_parser('GET b', DB)
        self.assertEqual(value, '2')
        _, DB, _ = command_parser('COMMIT', DB)
        self.assertEqual(DB, {"data": {'a': '2', 'b': '2'}, "transactions": []})
        stop, DB, value = command_parser('END', DB)
        self.assertEqual(stop, True)


if __name__ == '__main__':
    unittest.main()