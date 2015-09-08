from testtube.helpers import Flake8, Frosted, Helper, Nosetests, Pep257


class MakeDocs(Helper):
    command = 'make'
    all_files = True

    def get_args(self):
        return ['-C', 'docs/', 'html']


PATTERNS = (
    (r'((?!tests)(?!tube).)*\.py$', [Pep257(bells=0)]),
    (r'.*\.py$', [Flake8(all_files=True), Frosted(all_files=True)],
     {'fail_fast': True}),
    (r'(.*setup\.cfg$)|(.*\.coveragerc)|(.*\.py$)', [Nosetests()]),
    (r'.*\.rst$', [MakeDocs()])
)
