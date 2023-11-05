#from gcodeparser import GcodeParser
import sys
import re


#the richauto b11/a11 controller on the wood shop "axion precision iconic" CNC routers don't work correctly and needs metric
#without this post script on the gcode thise controlers it will read the G20 and use inches for x/y/z but NOT for the feed speed.  not sure about IJK.

fname = sys.argv[1]

isImperial = True


outputlines = []
outputlines.append('G21 (forced to metric by make_metric_gcode.py)')

regex = r'([A-Za-z])([-+]?(?:(?:\d+(?:\.\d*)?)|(?:\d*\.\d+)))'

with open(fname, 'r') as f:
  for line in f:

    #deal with comments
    outline=''
    parensopen = 0
    for c in line.rstrip():
      if c == ';' and not parensopen:
        break
      elif c=='(':
        parensopen += 1
      elif c==')':
        parensopen -= 1
      elif not parensopen:
        outline += c      
    line = outline


    #break up into command/register segments
    segs = line.split()
    newline = []
    for seg in segs:
#      print(seg)
      segparts = re.match(regex, seg)
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
        if letter.upper() == 'G' and number in [20,21]:
          if number == 20: #imperial
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




if '.' in fname:
  name,ext = sys.argv[1].rsplit('.', 1)
  newfilename = name + '_metric.' + ext
else:
  newfilename = fname + '_metric.nc'


with open(newfilename, 'w') as f:
  f.write('\n'.join(outputlines))
 
print('wrote', newfilename)


