from testtube.helpers import pep8_all, pyflakes_all, nosetests_all

PATTERNS = (
    (r'.*\.py', [nosetests_all, pep8_all, pyflakes_all]),
)
