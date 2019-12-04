from arg_parsers import parse_args_stat, parse_args_two
import run_chunk
import sys

def test_good_args1():
    sys.argv = 'arg_parsers.py -s mean'.split()
    args = parse_args_stat()
    assert(args.stat == 'mean')
    assert(args.stat != 'min')
    assert(args.stat != 'max')

def test_good_args2():
    try:
        sys.argv = 'arg_parsers.py -s mean -m BCC/bcc-csm1-1'.split()
        args = parse_args_two()
        assert(args.model == 'BCC/bcc-csm1-1')
    except AssertionError as exc:
        pass




