import unittest2

from querylist import BetterDict
from querylist.fieldlookup import (
    FieldLookup, FieldLookupCollection, field_lookup)


class FieldLookupTests(unittest2.TestCase):
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
        self.truthy_flc = FieldLookupCollection(
            foo=1, bar__cat=True, sauce__exact="Mustard")
        self.falsey_flc = FieldLookupCollection(
            foo=1, bar__cat=True, sauce__exact="mustard")


class FieldLookupParseLookupTests(FieldLookupTests):
    """FieldLookups._parse_lookup_string()"""
    def test_returns_single_value_list_for_simple_lookups(self):
        self.assertEquals(self.fl._parse_lookup_string('yay')[0], ['yay'])

    def test_splits_relational_lookups_properly(self):
        self.assertEquals(
            self.fl._parse_lookup_string('yay__bar')[0], ['yay', 'bar'])

    def test_defaults_to_exact_for_the_lookup_method(self):
        self.assertEquals(
            self.fl._parse_lookup_string('yay')[1], self.fl.exact)

    def test_correctly_determines_the_lookup_method_if_not_the_default(self):
        self.assertEquals(
            self.fl._parse_lookup_string('yay__iexact')[1], self.fl.iexact)


class FiedLookupResolveLookupChainTests(FieldLookupTests):
    """FieldLookup._resolve_lookup_chain()"""
    def test_returns_the_correct_value_for_simple_lookup_chains(self):
        self.assertEquals(
            self.fl._resolve_lookup_chain(['foo'], self.instance), 1)

    def test_returns_the_correct_value_for_multli_link_lookup_chains(self):
        self.assertEquals(
            self.fl._resolve_lookup_chain(['bar', 'dog'], self.instance),
            False
        )


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


class FieldLookUpCollectionEvaluation(FieldLookupTests):
    def test_returns_true_if_all_lookups_match(self):
        self.assertTrue(self.truthy_flc.evaluate(self.instance))

    def test_returns_false_if_any_lookups_fail(self):
        self.assertFalse(self.falsey_flc.evaluate(self.instance))
