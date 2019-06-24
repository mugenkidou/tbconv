# -*- coding: utf-8 -*-
import argparse
import re
import sys
import os.path


machine = 'unknown'
length = 16
triplet = 0
note = [24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,\
        24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24]
state = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
slide = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
accent = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
step = [0,0,0,0,0]
input_file = ""
output_file = ""

VERBOSE = False


## for test
#TODO: Remove global params

# length
def _set_length(val):
    global length
    length = val

def _get_length():
    return length

# triplet
def _set_triplet(val):
    global triplet
    triplet = val

def _get_triplet():
    return triplet

# note
def _set_note(val):
    global note
    note = val

def _get_note():
    return note

# state
def _set_state(val):
    global state
    state = val

def _get_state():
    return state

# slide
def _set_slide(val):
    global slide
    slide = val

def _get_slide():
    return slide

# accent
def _set_accent(val):
    global accent
    accent = val

def _get_accent():
    return accent

# step
def _set_step(val):
    global step
    step = val

def _get_step():
    return step

# input_file
def _set_input_file(val):
    global input_file
    input_file = val

def _get_input_file():
    return input_file

# output_file
def _set_output_file(val):
    global output_file
    output_file = val

def _get_output_file():
    return output_file

####

def vprint(lines, end='\n'):
    """Print lines verbosely.
    """
    if not VERBOSE:
        return
    if isinstance(lines, str):
        lines = [lines]
    for line in lines:
        print(line, end=end)


def getMachineType(line):
    if line.startswith('TRIPLET'):
         return 'TB-3'
    elif line.startswith('END_'):
        return 'TB-03'
    else:
        return 'unknown'


def readParam(line, machine):
    global length, triplet, step, note, state, slide, accent

    if line.startswith('END_'):
        length = int(re.split('[\(\t= ]', line.strip('\);\n'))[-1])

    elif line.startswith('LAST'):
        length = int(re.split('[\(\t= ]', line.strip('\);\n'))[-1])

    elif line.startswith('TRIPLET'):
        triplet = int(re.split('[\(\t= ]', line.strip('\);\n'))[-1])

    elif line.startswith('STEP '):
        step = line.replace('STEP ', '').replace('\t= STATE=',',').replace(' NOTE=',',').\
            replace(' ACCENT=',',').replace(' SLIDE=',',').replace('\n','').split(',')
        index = int(step[0])
        state[index-1] = int(not(int(step[1]))) # invert the value of step for TB-3
        note[index-1] = int(step[2])
        accent[index-1] = int(step[3])
        slide[index-1] = int(step[4])

    elif line.startswith('STEP'):
        step = line.replace('STEP', '').replace('(',',').strip('\);\n').split(',')
        index = int(step[0])
        note[index-1] = int(step[1])
        slide[index-1] = int(step[2])
        state[index-1] = int(not(int(step[3]))) # invert the value of step for TB-3
        accent[index-1] = int(step[4])


def writeParams(machine):
    global length, triplet, step, note, state, slide, accent, output_file
    if machine == 'TB-3':
        if length < 16:
            out_text1 = 'END_STEP\t= ' + str(length) + '\n'
            output_file1 = output_file
        else:
            out_text1 = 'END_STEP\t= 15\n'
            ofn = output_file.split('.')
            output_file1 = ofn[0] + 'a.' + ofn[1]
        out_text2 = 'END_STEP\t= ' + str(length-16) + '\n'
        out_text2 += 'TRIPLET\t= ' + str(triplet) + '\n'
        out_text1 += 'TRIPLET\t= ' + str(triplet) + '\n'
        for index in range(16):
            out_text1 += 'STEP ' + str(index+1) + \
                    '\t= STATE=' + str(state[index]) + \
                    ' NOTE=' + str(note[index]) + \
                    ' ACCENT=' + str(accent[index]) + \
                    ' SLIDE=' + str(slide[index]) + '\n'
        for index in range(16,32):
            out_text2 += 'STEP ' + str(index-15) + \
                    '\t= STATE=' + str(state[index]) + \
                    ' NOTE=' + str(note[index]) + \
                    ' ACCENT=' + str(accent[index]) + \
                    ' SLIDE=' + str(slide[index]) + '\n'

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
            ofn = output_file.split('.')
            output_file2 = ofn[0] + 'b.' + ofn[1]
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

            print(output_file1, 'and', output_file2, 'are generated instead of ', output_file, \
                ', because the pattern in', input_file, 'is longer than 16 steps.\n')
            
    elif machine == 'TB-03':
        out_text = 'TRIPLET(' + str(triplet) + ');\n'
        out_text += 'LAST_STEP(' + str(length) + ');\n'
        out_text += 'GATE_WIDTH(67);\n'
        for index in range(32):
            out_text += 'STEP' + str(index+1) + \
                        '(' + str(note[index]) + \
                        ',' + str(slide[index]) + \
                        ',' + str(state[index]) + \
                        ',' + str(accent[index]) + ');\n'
        out_text += 'BANK(0);\n'
        out_text += 'PATCH(-1);\n'
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
                '',
            ])

    print('Conversion complete.\n')


def main():
    global input_file

    if not(os.path.exists(input_file)):
        print('No such file: ', input_file)
        exit()

    with open(input_file,"rt") as prm:
        line = prm.readline()
        machine = getMachineType(line)
        
        if machine == 'unknown':
            print('Invalid file type.')
            exit()

        convert_to = 'TB-03' if machine == 'TB-3' else 'TB-3'
        print('Converting backup file from {} to {}\n'.format(machine, convert_to))

        readParam(line, machine)

        vprint([
            '----------',
            'Input File: {}'.format(input_file),
            '----------',
            '',
        ])

        while True:
            line = prm.readline()
            vprint([line], end='')
            readParam(line, machine)
            if not line:
                break

        writeParams(machine)


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

    main()
