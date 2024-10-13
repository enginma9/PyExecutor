## PyExecutor/Executor.py
It allows you to run commands from the top TextEdit, then when input is requested, the run button is replaced with an input area.  It captures stdout/err separately, and keeps a running log.  

The separate files are meant to be broken down and used in pieces, but all of it is usable from the Executor window.  
You can just create a CustomTextEdit by itself, which is being used for the code input, by opening your python console (`python3`/`py`), and calling:
```
>>> from CustomText import CustomTextEdit
>>> text_window = CustomTextEdit()
>>> text_window.show()
```

Normally you'd create QApplication first, but it's created in the first line of '__init__'.
( And you don't want to create another or QApplication running this program closes. )

You can use normal assignment for Qt/txt if you want to load a file to it:
```
>>> with open( "project.py", "r" ) as file:
>>>     text_window.setText( file.read() )
```

OpenCTE.py does the opening for you with a file chooser.  Nothing impressive, I just position it and turn off the frame to save screen space.  It does not save files on its own, as its just intended for reference, but you can save its content if you're running it from python console or Executor window:
```
from openCTE import text_window
TW = text_window()

#...

with open( "project.py", "w" ) as file:
    file.write( TW.toPlainText() )
```

Editor.py will have built-in functionality to save, but there are a million text editors out there you could copy into to save a file, so maybe not the most necessary thing for this project. 

## Styling
You can style/supply your own qss (like css, but slightly different with some syntax). It will take qss from whatever your cwd is, so you can have different appearances depending on what project directory you're running from (Feature not a bug, lol.)  It could be easily changed, if you want to overload it and add the File Dialog like in OpenCTE or save exact Qss path. You can even reload a stylesheet while its running:
```
styleFile = "/path/to/style.qss" 
with open(styleFile, "r") as fh: 
    window.setStyleSheet(fh.read())
```


### Working in same namespace
The globals for the exec calls are set that way on purpose.  This isn't a "customer-facing" app, its meant to be played with, so you can explore as much as if you were in the python console, and be able to edit whole functions before submitting them ( I always get frustrated when I made a mistake typing a function and have to start over. )

You can see that you can reference the code input area with code within the same window:
```
with open("nothings.py","r") as file:
    window.code_input.setText( file.read() )
# ( This just replaces the code in the input with text from file. )
```

I realize that makes it very breakable, but gives you a lot of flexibility and control over the window while its running.  
It would be fairly easy to create a separate .py file to create an instance with user-defined features every time it loads.  

*Side note: You can run more than one of these at a time so that they are separate processes.  
Having code you want to keep in a QTextEdit window attached to the one you're testing in, means if it crashes things, you lose the code too.  
You can even start a few text windows, close the code Executor, and not affect the windows.  

## Dont create new QApplication
One thing that will definitely crash this, is if you start a QApplication within it, because it is already running.  
That's why I package this if statement inside the class init, instead of an `if __name__ == '__main__':` : 
```
        if not QApplication.instance():
            self.app = QApplication( sys.argv )
```

## Testerwindow 
The Testerwindow.py is meant to add to the testing environment by easily adding buttons to correspond to commands, or TextEdits to hold code needed, etc.  A lot of its functionality can be easily done through some fairly simple Qt, but I just put a few convenience features in.  

You can run some of the text from Examples.py to demonstrate Testerwindow, and live edit the window while its running.

Frameless version window movement doesn't work through all OS, . 