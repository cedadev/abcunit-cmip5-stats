import run_chunk
import sys

def test_good_args1():
    sys.argv = 'run_chunk.py -s mean'.split()
    args = run_chunk.arg_parse_chunk()
    assert(args.stat == 'mean')
    assert(args.stat != 'min')
    assert(args.stat != 'max')


