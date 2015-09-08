from querylist import BetterDict
from querylist.fieldlookup import FieldLookup, field_lookup

from querylist.tests.base import TestCase


class FieldLookupTests(TestCase):
    def setUp(self):
        self.fl = FieldLookup()
        self.instance = BetterDict({
            'foo': 1,
            'bar': {
                'cat': True,
                'dog': False,
                'meh': {
                    'bleh': [1, 2]
                }
            },
            'sauce': 'Mustard',
            'bleh': [1, 2, 3, 4]
        })


class FieldLookupParseLookupTests(FieldLookupTests):
    """FieldLookups._parse_lookup_string()"""
    def test_returns_single_value_list_for_simple_lookups(self):
        self.assertEqual(self.fl._parse_lookup_string('yay')[0], ['yay'])

    def test_splits_relational_lookups_properly(self):
        self.assertEqual(
            self.fl._parse_lookup_string('yay__bar')[0], ['yay', 'bar'])

    def test_defaults_to_exact_for_the_lookup_method(self):
        self.assertEqual(
            self.fl._parse_lookup_string('yay')[1], self.fl.exact)

    def test_correctly_determines_the_lookup_method_if_not_the_default(self):
        self.assertEqual(
            self.fl._parse_lookup_string('yay__iexact')[1], self.fl.iexact)


class FiedLookupResolveLookupChainTests(FieldLookupTests):
    """FieldLookup._resolve_lookup_chain()"""
    def test_returns_the_correct_value_for_simple_lookup_chains(self):
        self.assertEqual(
            self.fl._resolve_lookup_chain(['foo'], self.instance), 1)

    def test_returns_the_correct_value_for_multli_link_lookup_chains(self):
        self.assertFalse(
            self.fl._resolve_lookup_chain(['bar', 'dog'], self.instance))


class FieldLookupCallTests(FieldLookupTests):
    """field_lookup()"""
    def test_returns_looked_up_value_when_passed_a_lookup_and_instance(self):
        self.assertEqual(
            field_lookup(self.instance, 'bar__meh__bleh'), [1, 2])

    def test_returns_comparison_result_when_compare_is_set_to_true(self):
        self.assertEqual(
            field_lookup(self.instance, 'foo', 1, True), True)

    def test_compares_based_on_comparator_specified_in_lookup_string(self):
        self.assertEqual(
            field_lookup(self.instance, 'sauce__iexact', 'mustard', True),
            True
        )
