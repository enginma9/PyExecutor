
commands_dict = {
    "create basic editor window":"""editor0 = editor_text_edit()\neditor0.show()""",
    "bring window to front":"""button_window.add_button( lambda: editor0.activateWindow(), "Show editor0" )""",
    "add button to testerwindow": """button_window.add_text_line( "line1" )""",
    "add a text edit field to the testerwindow":"""button_window.add_text_block( "block1" )""",
    "make testerwindow float permanently above others":"""button_window.setWindowFlags( button_window.windowFlags() | Qt.WindowStaysOnTopHint )""",
    "get text from file into QTextEdit/editor_text_edit":"""editor_0.setText( open( filename, "r" ).read() )""",
    "get name of lexer":"""get_lexer_by_name('C++') #make sure you: 'from pygments.styles import get_style_by_name' """,
    "change lexer":"""editor_x.highlighter.lexer = get_lexer_by_name('Python')\neditor_x.highlighter.rehighlight()""",
    "set text edit title":"""#editor_0.setWindowTitle('editor_0 - filename.py')""",
    "change text edit bg":"""#editor_0.set_bg_image( image_path_string ) # although you can also assign qss directly, and this may not work on all OS"""
}

examples = [''' 
def clip( text ): # Does not work with empty string: ""
    clipboard = QApplication.clipboard()
    clipboard.setText( text )

the_window = testerwindow()

def move_text( move_from, move_to ):
    the_window.item_dict[ move_to ].setText( the_window.get_text_from( move_from ) )

# Copy Button
the_window.add_button( lambda: clip( the_window.get_text_from( "Text Block 1" ) ), "Copy 1")
# QTextEdit
the_window.add_text_block( "Text Block 1" )
# Move button
the_window.add_button( lambda: move_text( "Text Block 1", "Text Block 2" ), "Move from 1 to 2")

# Copy Button
the_window.add_button( lambda: clip( the_window.get_text_from( "Text Block 2" ) ), "Copy 2")
# QTextEdit
the_window.add_text_block( "Text Block 2" )
# Move button
the_window.add_button( lambda: move_text( "Text Block 2", "Text Block 3" ), "Move from 2 to 3")

# Copy Button
the_window.add_button( lambda: clip( the_window.get_text_from( "Text Block 3" ) ), "Copy 3")
# QTextEdit
the_window.add_text_block( "Text Block 3" )
# Move button
the_window.add_button( lambda: move_text( "Text Block 3", "Text Block 4" ), "Move from 3 to 4")

# Copy Button
the_window.add_button( lambda: clip( the_window.get_text_from( "Text Block 4" ) ), "Copy 4")
# QTextEdit
the_window.add_text_block( "Text Block 4" )
# Move button
the_window.add_button( lambda: move_text( "Text Block 4", "Text Block 1" ), "Move from 4 to 1")
''',
'''def clip( text ): # Does not work with empty string: ""
clipboard = QApplication.clipboard()
clipboard.setText( text )

the_window = testerwindow()

def move_text( move_from, move_to ):
    the_window.item_dict[ move_to ].setText( the_window.get_text_from( move_from ) )

# Copy Button
the_window.add_button( lambda: clip( the_window.get_text_from( "Text Block 1" ) ), "Copy 1")
# QTextEdit
the_window.add_text_block( "Text Block 1" )
# Move button
the_window.add_button( lambda: move_text( "Text Block 1", "Text Block 2" ), "Move from 1 to 2")

# Copy Button
the_window.add_button( lambda: clip( the_window.get_text_from( "Text Block 2" ) ), "Copy 2")
# QTextEdit
the_window.add_text_block( "Text Block 2" )
# Move button
the_window.add_button( lambda: move_text( "Text Block 2", "Text Block 3" ), "Move from 2 to 3")

# Copy Button
the_window.add_button( lambda: clip( the_window.get_text_from( "Text Block 3" ) ), "Copy 3")
# QTextEdit
the_window.add_text_block( "Text Block 3" )
# Move button
the_window.add_button( lambda: move_text( "Text Block 3", "Text Block 4" ), "Move from 3 to 4")

# Copy Button
the_window.add_button( lambda: clip( the_window.get_text_from( "Text Block 4" ) ), "Copy 4")
# QTextEdit
the_window.add_text_block( "Text Block 4" )
# Move button
the_window.add_button( lambda: move_text( "Text Block 4", "Text Block 1" ), "Move from 4 to 1")
''',
'''def clip( text ): # Does not work with empty string: ""
clipboard = QApplication.clipboard()
clipboard.setText( text )''',
'''def move_text( move_from, move_to ):
the_window.item_dict[ move_to ].setText( the_window.get_text_from( move_from ) )
''','''
#Template 
import Divide
from Testerwindow import testerwindow
import os
this_window = Divide.Executor()
this_window.setStyleSheet( os.path.expanduser( '~/.Library/Executor/style.qss' ) )

def clip( text ): # Does not work with empty string: ""
    clipboard = QApplication.clipboard()
    clipboard.setText( text )

other_window = testerwindow()

def move_text( move_from, move_to ):
    other_window.item_dict[ move_to ].setText( other_window.get_text_from( move_from ) )

other_window.add_button( lambda: print( "#"*50 ), "#"*50 )

other_window.add_text_line( "Text Line 1" )
other_window.add_button( lambda: clip( other_window.get_text_from( "Text Block 1" ) ), "Copy 1")
other_window.add_text_block( "Text Block 1" )
'''
   
]

def print_example( x_number=0 ):
    global examples
    print( examples[ x_number ] )