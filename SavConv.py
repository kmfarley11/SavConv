#!/usr/bin/python3
#
# DETAILS:
#   Script to help with converting backed up saves to another format
#       i.e. raw nds .sav to .dsv for desmume
#   The above listed example(s) are the only supported ones for now
#       contributors are welcome, I only plan to update this per personal needs
#
# CONTRIB: 
#   Contributors are expected to update docstrings and follow PEP-8
#   I do not plan to personally test/regression test all options myself
#       it'd be easy enough to set up some CI/CD for this tho ¯\_(ツ)_/¯
#
# USAGE: 
#   python3 SavConv.py -h
#   python3 SavConv.py -i input.sav -o output.dsv
#

# imports and globals
import argparse
import os
import sys
import traceback


# list supported conversion posibilities...
# format of conversion string is <input-extension>2<output-extension>
SAV_TO_DSV = 'sav2dsv'
DSV_TO_SAV = 'dsv2sav'
SUPPORTED_CONVERSIONS = [SAV_TO_DSV, DSV_TO_SAV]

# TODO: add other relevant headers/footers/wrappers as necessary here...
DSV_FOOTER = \
    b'\x7c\x3c\x2d\x2d\x53\x6e\x69\x70\x20\x61\x62\x6f\x76\x65\x20\x68' \
    b'\x65\x72\x65\x20\x74\x6f\x20\x63\x72\x65\x61\x74\x65\x20\x61\x20' \
    b'\x72\x61\x77\x20\x73\x61\x76\x20\x62\x79\x20\x65\x78\x63\x6c\x75' \
    b'\x64\x69\x6e\x67\x20\x74\x68\x69\x73\x20\x44\x65\x53\x6d\x75\x4d' \
    b'\x45\x20\x73\x61\x76\x65\x64\x61\x74\x61\x20\x66\x6f\x6f\x74\x65' \
    b'\x72\x3a\x01\x00\x04\x00\x00\x00\x08\x00\x06\x00\x00\x00\x03\x00' \
    b'\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x7c\x2d\x44\x45\x53\x4d' \
    b'\x55\x4d\x45\x20\x53\x41\x56\x45\x2d\x7c'

# note: logger would be better than global verbose flag 
#   (maybe update that if this script grows...)
VERBOSE = False


class ConversionException(Exception):
    '''Custom exception to represent an issue during scripted conversion'''
    pass


def vprint(*args, **kwargs):
    '''Verbose printer, only print if verbose flag is set...'''
    if VERBOSE:
        print('[VERBOSE]', *args, **kwargs)


def get_supported_str(in_file, out_file):
    '''Helper to verify the conversion being attempted is a supported one
    
    Args:
        in_file (str) : filepath to save file to be converted
        out_file (str) : filepath to save file to be converted to

    Returns:
        conversion_type (str) : local conversion type tag formatted as
            '<input-extension>2<output-extension>'
    '''
    vprint('checking if inputted conversion is actually supported...')

    # from file paths inputted, extract the extension name for conversion_type
    try:
        in_ext = os.path.splitext(in_file)[-1].split('.')[-1]
        out_ext = os.path.splitext(out_file)[-1].split('.')[-1]
    except TypeError:
        raise ConversionException('Please input valid filepaths!')

    conversion_type = '{}2{}'.format(in_ext, out_ext)
    if conversion_type not in SUPPORTED_CONVERSIONS:
        raise ConversionException('{} not supported!'.format(conversion_type))

    print('Supported conversion found, going to try {}'.format(conversion_type))
    return conversion_type


def do_conversion(in_file, out_file):
    '''
    Main functionality: based on conversion attempt return new data
    
    Args:
        in_file (str) : filepath to save file to be converted
        out_file (str) : filepath to save file to be converted to

    Returns:
        None : no return, should except in case of failure else output created
    '''
    conversion_str = get_supported_str(in_file, out_file)

    vprint('attempting read of inputted file')
    if not os.path.exists(in_file):
        raise FileExistsError(in_file, 'not found, cannot attempt conversion!')

    in_data, out_data = b'', b''
    with open(in_file, 'rb') as f:
        in_data = f.read()
    
    # TODO: once this starts growing, create functions for each conversion...
    vprint('attempting conversion...')
    if conversion_str == SAV_TO_DSV:
        out_data = in_data + DSV_FOOTER
    
    elif conversion_str == DSV_TO_SAV:
        out_data = in_data.strip(DSV_FOOTER)

    # no else, check_supported raises if non-supported/invalid input

    vprint('attempting write to file...')
    with open(out_file, 'wb') as f:
        f.write(out_data.strip())


def main():
    '''Main method for python emulator save converter script'''
    parser = argparse.ArgumentParser()
    _a = parser.add_argument
    _a('--input-file', '-i', type=str, required=True,
        help='Input file to be converted (extension important!)')
    _a('--output-file', '-o', type=str, required=True,
        help='Output file to be converted to (extension important!)')
    _a('--verbose', '-v', action='store_true',
        help='Print extra output for script debugging etc.')
    args = parser.parse_args()

    # set up verbosity printing and display inputted args if applicable
    global VERBOSE
    VERBOSE = args.verbose
    vprint(args)

    try:
        do_conversion(args.input_file, args.output_file)
        print('Done.')
    
    except Exception:
        print('got exception during execution!...')
        traceback.print_exc(file=sys.stderr)
        print('see `python3 SavConv.py -h` for usage info', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

