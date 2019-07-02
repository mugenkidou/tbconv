# -*- coding: utf-8 -*-
import argparse
import enum
import re
import os.path


VERBOSE = False


class Machine(enum.Enum):
    """Machine types
    """
    TB3 = enum.auto()  # TB-3
    TB03 = enum.auto()  # TB-03
    UNKNOWN = enum.auto()


def vprint(lines, end='\n', verbose=None):
    """Print lines verbosely.
    """
    if verbose is None:
        verbose = VERBOSE
    if not verbose:
        return

    if isinstance(lines, str):
        lines = [lines]
    for line in lines:
        print(line, end=end)


def get_machine_type(line):
    """Detect machine type from first line of input file
    """
    if line.startswith('TRIPLET'):
        return Machine.TB3
    elif line.startswith('END_'):
        return Machine.TB03
    else:
        return Machine.UNKNOWN


def read_param(line, machine, length=16, triplet=0,
               note=[], state=[], slide=[], accent=[]):
    """Read one line and parse parameters.
    """
    if line.startswith('END_'):
        length = int(re.split(r'[\(\t= ]', line.strip(');\n'))[-1])

    elif line.startswith('LAST'):
        length = int(re.split(r'[\(\t= ]', line.strip(');\n'))[-1])

    elif line.startswith('TRIPLET'):
        triplet = int(re.split(r'[\(\t= ]', line.strip(');\n'))[-1])

    elif line.startswith('STEP '):
        step = line.replace('STEP ', '')\
                   .replace('\t= STATE=', ',')\
                   .replace(' NOTE=', ',')\
                   .replace(' ACCENT=', ',')\
                   .replace(' SLIDE=', ',')\
                   .replace('\n', '')\
                   .split(',')
        index = int(step[0])
        # invert the value of step for TB-3
        state[index-1] = int(not(int(step[1])))
        note[index-1] = int(step[2])
        accent[index-1] = int(step[3])
        slide[index-1] = int(step[4])

    elif line.startswith('STEP'):
        step = line.replace('STEP', '')\
                   .replace('(', ',')\
                   .strip(');\n')\
                   .split(',')
        index = int(step[0])
        note[index-1] = int(step[1])
        slide[index-1] = int(step[2])
        # invert the value of step for TB-3
        state[index-1] = int(not(int(step[3])))
        accent[index-1] = int(step[4])

    return length, triplet, note, state, slide, accent


def write_params(machine, output_file, length, triplet,
                 note, state, slide, accent):
    """Write pattern to output_file.
    """
    if machine == Machine.TB3:
        out_lines_1 = []
        out_lines_2 = []

        # END_STEP
        if length < 16:
            out_lines_1.append('END_STEP\t= {}'.format(length))
            output_file1 = output_file
        else:
            out_lines_1.append('END_STEP\t= 15')

            # output_file name
            ofn = output_file.split('.')
            # TODO: check no '.'
            output_file1 = '{}a.{}'.format(ofn[0], ofn[1])
            output_file2 = '{}b.{}'.format(ofn[0], ofn[1])

        out_lines_2.append('END_STEP\t= {}'.format(length - 16))

        # TRIPLET
        out_lines_1.append('TRIPLET\t= {}'.format(triplet))
        out_lines_2.append('TRIPLET\t= {}'.format(triplet))

        # STEPs
        for index in range(16):
            out_lines_1.append(
                'STEP {}\t= STATE={} NOTE={} ACCENT={} SLIDE={}'.format(
                    index + 1,
                    state[index],
                    note[index],
                    accent[index],
                    slide[index],
                ))
        for index in range(16, 32):
            out_lines_2.append(
                'STEP {}\t= STATE={} NOTE={} ACCENT={} SLIDE={}'.format(
                    index - 15,
                    state[index],
                    note[index],
                    accent[index],
                    slide[index],
                ))

        out_text1 = '\n'.join(out_lines_1) + '\n'
        with open(output_file1, 'wt') as outf:
            outf.write(out_text1)
            vprint([
                '',
                '----------',
                'Output file: {}'.format(output_file1),
                '----------',
                '',
                out_text1,
            ])

        if length > 15:
            out_text2 = '\n'.join(out_lines_2) + '\n'
            with open(output_file2, 'wt') as outf:
                outf.write(out_text2)

            vprint([
                '----------',
                'Output file: {}'.format(output_file2),
                '----------',
                '',
                out_text2,
                '----------',
                '',
            ])

            print((
                '{} and {} are generated instead of {}, '
                'because the pattern in input file is longer than 16 steps.\n'
            ).format(
                output_file1, output_file2, output_file,
            ))

    elif machine == Machine.TB03:
        out_lines = []
        out_lines.append('TRIPLET({});'.format(triplet))
        out_lines.append('LAST_STEP({});'.format(length))
        out_lines.append('GATE_WIDTH(67);')

        for index in range(32):
            out_lines.append(
                'STEP{}({},{},{},{});'.format(
                    index+1,
                    note[index],
                    slide[index],
                    state[index],
                    accent[index],
                ))

        out_lines.append('BANK(0);')
        out_lines.append('PATCH(-1);')

        out_text = '\n'.join(out_lines) + '\n'
        with open(output_file, 'wt') as outf:
            outf.write(out_text)

            vprint([
                '',
                '----------',
                'Output file: {}'.format(output_file),
                '----------',
                '',
                out_text,
                '----------',

            ])


def main(input_file, output_file):
    if not(os.path.exists(input_file)):
        print('No such file: {}'.format(input_file))
        return

    with open(input_file, "rt") as prm:
        line = prm.readline()
        machine = get_machine_type(line)

        if machine == Machine.UNKNOWN:
            print('Invalid file type.')
            exit()

        convert_to = Machine.TB03 if machine == Machine.TB3 else Machine.TB3
        print('Converting backup file from {} to {}\n'.format(
            machine.name, convert_to.name))

        length = 16
        triplet = 0
        note = [
            24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24,
        ]
        state = [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        ]
        slide = [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        ]
        accent = [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        ]
        length, triplet, note, state, slide, accent = read_param(
            line, machine, length, triplet, note, state, slide, accent)

        vprint([
            '----------',
            'Input File: {}'.format(input_file),
            '----------',
            '',
        ])

        while True:
            line = prm.readline()
            vprint([line], end='')
            length, triplet, note, state, slide, accent = read_param(
                line, machine, length, triplet, note, state, slide, accent)
            if not line:
                break

        write_params(
            machine, output_file, length, triplet, note, state, slide, accent)

    print('Conversion complete.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'INPUT_FILE',
        help='File to convert.',
    )
    parser.add_argument(
        'OUTPUT_FILE',
        help='The result of file conversion.',
    )
    parser.add_argument(
        '-p', '--print',
        action='store_true',
        dest='verbose',
        help='Print input and output file.',
    )
    args = parser.parse_args()

    input_file = args.INPUT_FILE
    output_file = args.OUTPUT_FILE
    VERBOSE = args.verbose

    main(input_file, output_file)
