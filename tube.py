import subprocess
from testtube.helpers import pep8_all, pyflakes_all, nosetests_all


def make_docs(changed, **kwargs):
    print 'Regenerating documentation...\n'
    subprocess.call(['make', '-C', 'docs/', 'html'])


PATTERNS = (
    (r'.*\.py', [nosetests_all, pep8_all, pyflakes_all, make_docs]),
    (r'(?P<path>.*)\.rst', [make_docs]),
)
