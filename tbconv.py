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
pFlag = False


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
    global length, triplet, step, note, state, slide, accent, output_file, pFlag
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
            if pFlag == True:
                print('\n----------\nOutput file:', output_file1, '\n----------\n')
                print(out_text1)

        if length > 15:
            ofn = output_file.split('.')
            output_file2 = ofn[0] + 'b.' + ofn[1]
            with open(output_file2, 'wt') as outf:
                outf.write(out_text2)
            if pFlag == True:
                print('----------\nOutput file:', output_file2, '\n----------\n')
                print(out_text2)
                print('----------\n')
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
            if pFlag == True:
                print('\n----------\nOutput file:', output_file, '\n----------\n')
                print(out_text)
                print('----------\n')
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

        print('Converting backup file from ', machine, ' to ', end='')
        if machine == 'TB-3':
            print('TB-03.\n')
        else:
            print('TB-3.\n')
        readParam(line, machine)

        if pFlag == True:
            print('----------\nInput File:', input_file, '\n----------\n')
        while True:
            line = prm.readline()
            if pFlag == True:
                print(line, end='')
            readParam(line, machine)
            if not line:
                break

        writeParams(machine)

def getArgs():
    global input_file, output_file, pFlag
    arguments = sys.argv

    if len(arguments) < 3 or len(arguments) > 4:
        return False
    if arguments[1].startswith('-') or arguments[2].startswith('-'):
        print('-\n')
        return False

    input_file = arguments[1]
    output_file = arguments[2]
    if len(arguments) == 4:
        if arguments[3] == '-p' or arguments[3] == '--print':
            pFlag = True
        else:
            return False
    return True

if __name__ == '__main__':
    if getArgs() == True:
        main()
    else:
        print('Usage: python {} INPUT_FILE OUTPUT_FILE [--print]\n'.format(__file__))
