Overly hackable testing interface.  
Executor window meant to be used like an extension for Python Console. 
Its meant to be flexible, to the point you can break it if you choose.  

It allows you to run commands from the top TextEdit, then when input is requested, the run button is replaced with an input area.  It captures stdout/err separately, and keeps a running log.  

The separate files are meant to be broken down and used in pieces, but all of it is usable from the Executor window.  
You can just create a CustomTextEdit by itself by opening your python console (`python3`/`py`), and calling and showing:
```
>>> from CustomText import CustomTextEdit
>>> text_window = CustomTextEdit()
>>> text_window.show()
```
Normally you'd create QApplication first, but it's created in the first line of '__init__'.
you can use normal assignment if you want to load a file to it:
```
>>> with open( "project.py", "r" ) as file:
>>>     text_window.setText( file.read() )
```
OpenCTE.py just does that for you with a file chooser.  Nothing impressive, I just position it and turn off the frame to save screen space.  It does not save files on its own, as its just intended for reference, but you can save its content if you're running it from python console or Executor window:
```
from openCTE import text_window
TW = text_window()

#...

with open( "project.py", "w" ) as file:
    file.write( TW.toPlainText() )
```

Interface written in only python, except Qt resources.
Have used with PyQt5/6 and PySide6.  Generally you can swap PyQt5/PySide6, but will have to move QAction's import text from QtWidgets to I believe QtGui, then it should run.  


The globals for the exec calls are set that way on purpose.  This isn't a "customer-facing" app, its meant to be played with, so you can explore as much as if you were in the python console, but able to edit whole functions before submitting them ( I always get frustrated when I made a mistake typing a function and have to start over. )

You can style/supply your own qss (like css, but slightly different with some syntax). It will take qss from whatever your cwd is, so you can have different appearances depending on what project directory you're running from (Feature not a bug, lol.)  It could be easily changed, if you want to overload it and add the File Dialog like in OpenCTE or save exact Qss path. You can even reload a stylesheet while its running:
```
styleFile = "/path/to/style.qss" 
with open(styleFile, "r") as fh: 
    window.setStyleSheet(fh.read())
```
You can see that you can reference the code input area with code within the same window:
```
with open("nothings.py","r") as file:
    window.code_input.setText( file.read() )
# ( This just replaces the code in the input with text from file. )
```

I realize that makes it very breakable, but gives you a lot of flexibility and control over the window while its running.  
It would be fairly easy to create a separate .py file to create an instance with user-defined features every time it loads.  

The primary reason I made this is that I didn't want to use too many calls to APIs or feeds just because of testing, when I could keep the retrieved info in memory and keep working with it easily without it being one line at a time from the console.  

The Testerwindow.py is somewhat a completely different thing, Its meant to add to the testing environment by easily adding buttons to correspond to commands, or TextEdits to hold code needed, etc.  
You can run some of the text from Examples.py to demonstrate Testerwindow, and live edit the window while its running.

Frameless version dragging doesn't work through all OS, so use at your own risk.  I'm probably going to remove it at some point.
