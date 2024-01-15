# What is this

Converts a gcode file to all "G21" / metric / millimeters.
    
The Richauto A11/B11 controller on the wood shop "axion precision iconic" CNC routers don't work correctly with inch units. 
    
Without this post-processing script those controllers will read the G20 and use inches for X/Y/Z but NOT for the feed speed.  I'm not sure what it does about IJK.
    
This script works by replacing any G20 (inch) sections of the gcode with G21 (millimeter) versions of the numbers.  Command codes modified are A, B, C, F, I, J, K, R, U, V,
    
If no G20 is in your gcode, this script will not assume inches and it will do nothing.  You could add a G20 at the top of your code and try again.
    
Comments are currently lost in the output because I'm lazy.


# Install
Just download and run the releases built on github. https://github.com/Brown-County-FIRST-Robotics/MakeMetricGcode/releases/latest

## If you downloaded the source
```bash
git clone  git@github.com:Brown-County-FIRST-Robotics/MakeMetricGcode.git
cd MakeMetricGcode
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

# Run
If you have a downloaded release executable just run it

## If you downloaded the source
```bash
python guimain.py 
```


# Build
## Using github actions to make a release with windows and linux asssets
create a release in github.  A workflow in .github/workflows/release.yml will build the artifacts and stick them on the release
## Linux
```bash
. venv/bin/activate
pip install -r requirements.txt
pip install -r build_requirements.txt
pyinstaller -F guimain.py -n make_metric_gcode
```

# Todo
- [x] build linux release
- [x] build windows release
- [ ] build mac release
- [ ] better GUI style: https://www.reddit.com/r/Python/comments/lps11c/how_to_make_tkinter_look_modern_how_to_use_themes/
- [ ] stop using easygui or fix the extension ordering in file open and save dialog
- [ ] ignore dot files: https://stackoverflow.com/questions/53220711/how-to-avoid-hidden-files-in-file-picker-using-tkinter-filedialog-askopenfilenam

