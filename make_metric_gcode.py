import re

def process(gcode):
    '''Converts a gcode file to all "G21" / metric / millimeters.

The Richauto A11/B11 controller on the wood shop "axion precision iconic" CNC routers don't work correctly with inch units.

Without this post-processing script those controllers will read the G20 and use inches for X/Y/Z but NOT for the feed speed.  I'm not sure what it does about IJK.

This script works by replacing any G20 (inch) sections of the gcode with G21 (millimeter) versions of the numbers.  Command codes modified are A, B, C, F, I, J, K, R, U, V, W, X, Y, Z.

If no G20 is in your gcode, this script will not assume inches and it will do nothing.  You could add a G20 at the top of your code and try again.

Comments are currently lost in the output because I'm lazy.'''

    isImperial = True

    outputlines = []
    outputlines.append('G21 (forced to metric by make_metric_gcode.py)')

    regex = re.compile(r'([A-Za-z])([-+]?(?:(?:\d+(?:\.\d*)?)|(?:\d*\.\d+)))')

    for line in gcode.split('\n'):

        # deal with comments
        outline = ''
        parensopen = 0
        for c in line.rstrip():
            if c == ';' and not parensopen:
                break
            elif c == '(':
                parensopen += 1
            elif c == ')':
                parensopen -= 1
            elif not parensopen:
                outline += c
        line = outline

        # break up into command/register segments
        segs = line.split()
        newline = []
        for seg in segs:
            #      print(seg)
            segparts = regex.match(seg)
            if segparts is None:
                newline.append(seg)
            else:
                #        print(segparts.groups())
                letter, number = segparts.groups()
                isfloat = '.' in number
                if isfloat:
                    number = float(number)
                else:
                    number = int(number)
                if letter.upper() == 'G' and number in [20, 21]:
                    if number == 20:  # imperial
                        isImperial = True
                    else:
                        isImperial = False
                        continue

                #          print(letter, number)
                if letter.upper() in 'ABCFIJKRUVWXYZ' and isImperial:
                    number *= 25.4

                if isfloat:
                    newline.append('%s%.3f' % (letter, number))
                else:
                    newline.append('%s%u' % (letter, number))

        #        print(letter, number)
        outputlines.append(' '.join(newline))

    return '\n'.join(outputlines)


def suggestname(oldname):
    if '.' in oldname:
        name, ext = oldname.rsplit('.', 1)
        newfilename = name + '_metric.' + ext
    else:
        newfilename = oldname + '_metric.nc'
    return newfilename

if __name__ == '__main__':
    import sys

    fname = sys.argv[1]
    with open(fname, 'r') as f:
        gcode = f.read()

    output = process(gcode)

    newfilename = suggestname(fname)
    with open(newfilename, 'w') as f:
        f.write('\n'.join(output))

    print('wrote', newfilename)
