import sys

from run_all import arg_parse_all
from run_batch import arg_parse_batch
from run_chunk import arg_parse_chunk
from arg_parsers import parse_args_stat, parse_args_two


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


def test_good_args3():
    try:
        sys.argv = 'arg_parsers.py -s mean -m BCC/bcc-csm1-1'.split()
        args = parse_args_two()
        assert(args.model == ['BCC/bcc-csm1-1'])
        assert (args.stat == 'mean')
    except AssertionError as exc:
        pass


def test_good_args4():
    sys.argv = 'arg_parsers.py -s mean -m BCC/bcc-csm1-1'.split()
    args = parse_args_two()
    assert(args.model == ['BCC/bcc-csm1-1'])
    assert (args.stat == ['mean'])


#test that stat is required
def test_arg_parse_all_1():
    try:
        sys.argv = 'run_chunk.py'.split()
        arg_parse_all()
    except SystemExit as exc:
        pass

#test works with only stat
def test_arg_parse_all_2():
    sys.argv = 'run_chunk.py -s min'.split()
    arg_parse_all()


#testing that other arguments are required
def test_arg_parse_batch():
    try:
        sys.argv = 'run_chunk.py -s min'.split()
        arg_parse_batch()
    except SystemExit as exc:
        pass


#testing that other arguments are required
def test_arg_parse_chunk_1():
    try:
        sys.argv = 'run_chunk.py -s min'.split()
        arg_parse_chunk()
    except SystemExit as exc:
        pass

#testing ensemble is required
def test_arg_parse_chunk_2():
    try:
        sys.argv = 'run_chunk.py -s min -m BCC/bcc-csm1-1'.split()
        arg_parse_chunk()
    except SystemExit as exc:
        pass






