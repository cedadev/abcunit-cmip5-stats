import sys

from lib import defaults
import run_all


#testing print statement is correct
def test_running_print_statement():
    sys.argv = 'run_all.py -s mean -m BCC/bcc-csm1-1 -e r10i1p1 -v baresoilFrac'.split()
    statement = print(run_all.main())
    assert(statement=="Finding ['mean'] of baresoilFrac for BCC/bcc-csm1-1, r10i1p1.")
