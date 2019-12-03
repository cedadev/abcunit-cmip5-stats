from run_stuff import parse_args
import sys

def test_good_args1():
    sys.argv = 'run_stuff.py -s mean'.split()
    args = parse_args()
    assert(args.stat == 'mean')
    assert(args.stat != 'min')
    assert(args.stat != 'max')	
