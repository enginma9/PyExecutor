
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
''',
   
]

def print_example( x_number=0 ):
    global examples
    print( examples[ x_number ] )