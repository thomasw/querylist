from querylist.fieldlookup import FieldLookup

from tests.base import TestCase

fl = FieldLookup


class ExactTests(TestCase):
    """FieldLookup.exact()"""
    def test_returns_true_if_passed_values_match_exactly(self):
        self.assertTrue(fl.exact(1, 1))

    def test_returns_false_if_passed_values_dont_match(self):
        self.assertFalse(fl.exact(1, 2))


class IExactTests(TestCase):
    """FieldLookup.iexact()"""
    def test_returns_true_if_case_insensitive_values_match(self):
        self.assertTrue(fl.iexact('Yay', 'yay'))

    def test_returns_false_if_values_dont_match(self):
        self.assertFalse(fl.iexact('yay', 'foo'))


class ContainsTests(TestCase):
    """FieldLookup.contains()"""
    def test_returns_true_if_first_value_contains_second_value(self):
        self.assertTrue(fl.contains('go team', 'team'))

    def test_returns_true_if_first_list_contains_second_list(self):
        self.assertTrue(fl.contains([1, 2], 2))

    def test_returns_false_if_first_value_does_not_contain_second(self):
        self.assertFalse(fl.contains([1, 2], 3))


class IContainsTests(TestCase):
    """FieldLookup.icontains()"""
    def test_returns_true_if_first_value_contains_second_with_any_case(self):
        self.assertTrue(fl.icontains('FLOrida', 'flo'))

    def test_returns_False_if_first_value_doesnt_contain_second_value(self):
        self.assertFalse(fl.icontains('Florida', 'Cal'))


class InTests(TestCase):
    """FieldLookup.in()"""
    def test_returns_true_if_first_value_is_in_second_value(self):
        self.assertTrue(fl.isin(1, [1, 2]))

    def test_returns_false_if_second_value_does_not_contain_first_value(self):
        self.assertFalse(fl.isin(4, [1, 2]))


class StartsWithTests(TestCase):
    """FieldLookup.startswith()"""
    def test_returns_true_if_first_value_starts_with_second_value(self):
        self.assertTrue(fl.startswith('kittens', 'kitten'))

    def test_returns_false_if_first_value_doesnt_start_with_second(self):
        self.assertFalse(fl.startswith('kittens', 'do'))


class IStartsWithTests(TestCase):
    """FieldLookup.istartswith()"""
    def test_lowercase_vals_and_return_true_if_first_starts_with_second(self):
        self.assertTrue(fl.istartswith('Kittens', 'kitteN'))

    def test_returns_false_if_first_value_doesnt_start_with_second(self):
        self.assertFalse(fl.istartswith('Kittens', 'DOG'))


class EndsWithTests(TestCase):
    """FieldLookup.endswith()"""
    def test_returns_true_if_first_value_ends_with_second_value(self):
        self.assertTrue(fl.endswith('kittens', 'tens'))

    def test_returns_false_if_first_value_doesnt_end_with_second(self):
        self.assertFalse(fl.endswith('kittens', 'do'))


class IEndsWithTests(TestCase):
    """FieldLookup.iendswith()"""
    def test_lowercase_vals_and_return_true_if_first_ends_with_second(self):
        self.assertTrue(fl.iendswith('Kittens', 'teNs'))

    def test_returns_false_if_first_value_doesnt_end_with_second(self):
        self.assertFalse(fl.iendswith('Kittens', 'DOG'))


class RegexTests(TestCase):
    """FieldLookup.regex()"""
    def test_returns_true_if_first_value_matches_regex(self):
        self.assertTrue(fl.regex('foo', r'\w*'))

    def test_returns_false_if_first_value_doesnt_match_regex(self):
        self.assertFalse(fl.regex('foo', r'\w*BOOP'))


class IRegexWithTests(TestCase):
    """FieldLookup.iregex()"""
    def test_returns_true_if_first_value_matches_iregex(self):
        self.assertTrue(fl.iregex('foo', r'[A-Z]*'))

    def test_returns_false_if_first_value_doesnt_match_iregex(self):
        self.assertFalse(fl.iregex('foo', r'[A-Z]*BOOP'))


class GTTests(TestCase):
    """FieldLookup.gt()"""
    def test_returns_true_if_first_value_is_greater_than_second(self):
        self.assertTrue(fl.gt(2, 1))

    def test_returns_false_if_first_value_isnt_greater_than_second(self):
        self.assertFalse(fl.gt(1, 2))

    def test_returns_false_if_values_are_equal(self):
        self.assertFalse(fl.gt(2, 2))


class GTETests(TestCase):
    """FieldLookup.gte()"""
    def test_returns_true_if_first_value_is_greater_than_second(self):
        self.assertTrue(fl.gte(2, 1))

    def test_returns_true_if_values_are_equal(self):
        self.assertTrue(fl.gte(2, 2))

    def test_returns_false_if_first_value_isnt_greater_than_second(self):
        self.assertFalse(fl.gte(1, 2))


class LTTests(TestCase):
    """FieldLookup.lt()"""
    def test_returns_true_if_first_value_is_less_than_second(self):
        self.assertTrue(fl.lt(1, 2))

    def test_returns_false_if_first_value_isnt_less_than_second(self):
        self.assertFalse(fl.lt(3, 2))

    def test_returns_false_if_values_are_equal(self):
        self.assertFalse(fl.lt(2, 2))


class LTETests(TestCase):
    """FieldLookup.lte()"""
    def test_returns_true_if_first_value_is_less_than_second(self):
        self.assertTrue(fl.lte(1, 2))

    def test_returns_false_if_first_value_isnt_less_than_second(self):
        self.assertFalse(fl.lte(3, 2))

    def test_returns_true_if_values_are_equal(self):
        self.assertTrue(fl.lte(2, 2))
