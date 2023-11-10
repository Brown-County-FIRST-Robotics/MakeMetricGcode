import easygui


def main():
    title = 'Make Metric GCode postprocessor'

    extraMessage = ''

    try:
        while 1:
            extra = '' if not extraMessage else ('\n\n' + extraMessage)
            choice = easygui.buttonbox(msg=f'{title} - \n\nMake a gcode file into all metric{extra}', title=title,
                                       choices=('Select File', 'About / Help', 'Exit'), default_choice='Select File', cancel_choice='Exit')
            if choice == 'About / Help':
                easygui.textbox(msg='About', title=title, text='''Converts a gcode file to all "G21" / metric / millimeters.
    
    The Richauto A11/B11 controller on the wood shop "axion precision iconic" CNC routers don't work correctly with inch units. 
    
    Without this post-processing script those controllers will read the G20 and use inches for X/Y/Z but NOT for the feed speed.  I'm not sure what it does about IJK.
    
    This script works by replacing any G20 (inch) sections of the gcode with G21 (millimeter) versions of the numbers.  Command codes modified are A, B, C, F, I, J, K, R, U, V, W, X, Y, Z.
    
    If no G20 is in your gcode, this script will not assume inches and it will do nothing.  You could add a G20 at the top of your code and try again.
    
    Comments are currently lost in the output because I'm lazy.
    ''')
                extraMessage = ''
            elif choice == 'Select File':
                fname = easygui.fileopenbox(msg='Select file to process', title=title,
                                            filetypes=[['*.nc', '*.NC', '*.gc', '*.GC', 'gcode files'], ['*.*', 'All files']], multiple=False)
                if fname is None:
                    extraMessage = ''
                    continue
                import make_metric_gcode

                try:

                    with open(fname, 'r') as f:
                        gcode = f.read()

                    extents={}
                    output = make_metric_gcode.process(gcode, extents)

                    newfilename = make_metric_gcode.suggestname(fname)

                    newfilename = easygui.filesavebox(msg='Save result as', title=title, default=newfilename,
                                                      filetypes=[['*.nc', '*.NC', '*.gc', '*.GC', 'gcode files'], ['*.*', 'All files']])
                    if newfilename is None:
                        extraMessage = 'Last file canceled'
                        continue

                    with open(newfilename, 'w') as f:
                        f.write('\n'.join(output))

                except:
                    easygui.exceptionbox(title=title, msg='failure processing this gcode file')
                    extraMessage = 'Last file failed'

                extraMessage = 'File processed and saved\nExtents in mm:\n'
                for letter, (mn, mx) in sorted(extents.items()):
                    extraMessage += f'{letter}: {mn} to {mx}\n'

            else:
                break

    except:
        easygui.exceptionbox(title=title, msg='general failure')

if __name__ == '__main__':
    main()
