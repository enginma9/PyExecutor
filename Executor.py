# Import PyQt resources
from PyQt5.QtWidgets import ( QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLineEdit, QLabel, QTextEdit, QListWidget, QTabWidget, QMenu, 
    QPlainTextEdit, QAction, QAbstractItemView, QDialog )
from PyQt5.QtGui import QClipboard, QFont, QCursor, QTextCursor
from PyQt5.QtCore import Qt
# Other Libraries
import sys
import io
# This project 
from CustomText import CustomTextEdit
from Helpers import get_globals, print_attributes, print_keys, print_nested, get_nested_keys
from OutputRedirect import OutputRedirector
from Testerwindow import testerwindow
from Examples import print_example

# QTextEdit -> CustomTextEdit
# QPlainTextEdit still uses toPlainText(), so no change needed there
# but will need to use QPlainTextEdit.setPlainText( string ) to set text
# insertPlainText() if needing a log or .appendPlainText(text)

# setWordWrapMode( setting )
# QTextOption::NoWrap	                    0	Text is not wrapped at all.
# QTextOption::WordWrap	                    1	Text is wrapped at word boundaries.
# QTextOption::ManualWrap	                2	Same as QTextOption::NoWrap
# QTextOption::WrapAnywhere	                3	Text can be wrapped at any point on a line, even if it occurs in the middle of a word.
# QTextOption::WrapAtWordBoundaryOrAnywhere	4	If possible, wrapping occurs at a word boundary; otherwise it will occur at the appropriate point on the line, even in the middle of a word.

# Set up context menu to allow for other options, possibly zoom https://doc.qt.io/qt-6/qplaintextedit.html#public-slots
# void 	appendHtml(const QString &html)
# void 	appendPlainText(const QString &text)
# void 	centerCursor()
# void 	clear()
# void 	copy()
# void 	cut()
# void 	insertPlainText(const QString &text)
# void 	paste()
# void 	redo()
# void 	selectAll()
# void 	setPlainText(const QString &text)
# void 	undo()
# void 	zoomIn(int range = 1)
# void 	zoomOut(int range = 1)

# Additional methods: clear() - clear all text and listwidgets, 
# testerwindow.del( text ) remove the item, whether it is a button/textEdit/PlainTextEdit/etc.
# Encapsulate codebox and button in a Vert layout so that the bigger layout can be changed out to a horizonal layout, putting code & tabs next to each other
# create testerwindow.set_new_stylesheet()

# buttons to add commands for you
# button to get globals
# listwidget to display globals
# double-click to insert into cursor position in text box
# button to query any object

class CodeExecutorWindow( QDialog ):
    """
    A PyQt5 window with a text box to input Python code and a button to execute the code in the console.
    
    Run this python file directly to get the CodeExecutorWindow window, or import it from python console, and:
        `import Executor`
        `window = Executor.CodeExecutorWindow()`
        - or -
        `from Executor import CodeExecutorWindow`
        `window = CodeExecutorWindow()`

        You don't have to do the normal `app = QApplication( sys.argv )` as it is done in the __init__
    You can also try frameless_executor.py

    """
    def __init__( self ):
        if not QApplication.instance():
            self.app = QApplication( sys.argv )
        super().__init__()
        # 
        self.shared_namespace = globals()

        # Set Style
        try:
            styleFile = "style.qss" 
            with open(styleFile, "r") as fh: 
                self.setStyleSheet(fh.read())
        except:
            pass

        # Base
        # Set up the layout
        self.layout = QVBoxLayout( self )

        # Top
        # Text box for user to input Python code
        self.code_input = CustomTextEdit( self )
        self.layout.addWidget( self.code_input )

        # Button to execute the Python code
        self.run_button = QPushButton( "Run Code", self )
        self.layout.addWidget( self.run_button )
        
        # Mid
        #QVBoxLayout with 4 labels
        self.label_box = QHBoxLayout()
        
        self.cur_lc_label  = QLabel("Cursor")
        self.cur_lc_label.setAlignment(Qt.AlignLeft)
        self.label_box.addWidget( self.cur_lc_label )
        
        self.cur_ch_label = QLabel("0x0, 0")
        self.cur_ch_label.setAlignment(Qt.AlignCenter)
        self.label_box.addWidget( self.cur_ch_label )
        
        self.end_lc_label = QLabel("End")
        self.end_lc_label.setAlignment(Qt.AlignCenter)
        self.label_box.addWidget( self.end_lc_label )
        
        self.end_ch_label = QLabel("0x0, 0")
        self.end_ch_label.setAlignment(Qt.AlignRight)
        self.label_box.addWidget( self.end_ch_label )
        # Set code for labels:
        self.code_input.cursorPositionChanged.connect( self.set_curr )
        self.code_input.textChanged.connect( self.set_end )
        #self.code_input.selectionChanged.connect()
        
        # divide out widgets above & below, or put this into a widget first:
        temp_widget = QWidget()
        #temp_widget.setContentsMargins( 0,0,0,0 )
        temp_widget.setLayout( self.label_box )
        #self.label_box.setContentsMargins( 0,0,0,0 )
        self.layout.addWidget( temp_widget )

        # Hidden Input
        self.input_line = QLineEdit(self)
        self.input_line.setPlaceholderText("Input)")
        self.input_line.setEnabled(False)  # Disabled until input() is called
        self.layout.addWidget(self.input_line)
        self.input_line.hide()

        # Connect Enter key to simulate input
        self.input_line.returnPressed.connect( self.submit_input )

        self.shared_namespace.update({"input": self.input_line})
        #########################
        # Bottom
        #########################

        # Create a tab widget
        self.tab_widget = QTabWidget( self )
        self.layout.addWidget( self.tab_widget )

        #########################
        # Tab 1
        #########################

        # First tab for output and error lists
        self.output_error_tab = QWidget()
        self.output_error_layout = QVBoxLayout( self.output_error_tab )
        # Add tab to tab widget
        self.tab_widget.addTab( self.output_error_tab, "stdout/stderr" )
        

        # List widgets for output and errors in the first tab
        self.output_list = QListWidget( self )
        self.error_list = QListWidget( self )
        # Style
        self.output_list.setAlternatingRowColors( True )
        self.error_list.setAlternatingRowColors( True )
        # Place
        self.output_error_layout.addWidget( self.output_list )
        self.output_error_layout.addWidget( self.error_list )

        #########################
        # Tab 2
        #########################
        # Second tab for combined log
        self.combined_tab = QWidget()
        self.combined_layout = QVBoxLayout( self.combined_tab )
        # Add tab to tab widget
        self.tab_widget.addTab( self.combined_tab, "Log" )

        # Combined list widget in the second tab
        self.combined_list = QListWidget( self )
        self.combined_list.setAlternatingRowColors( True )
        self.combined_layout.addWidget( self.combined_list )
        self.clr_comb_button = QPushButton( "Clear", self )
        self.combined_layout.addWidget( self.clr_comb_button )
        self.clr_comb_button.clicked.connect( self.clear_combined )

        ###########################
        # Context / Scroll in tabs
        ###########################

        # Enable context menu for all list widgets
        self.output_list.setContextMenuPolicy( Qt.CustomContextMenu )
        self.output_list.customContextMenuRequested.connect( self.show_context_menu )
        self.output_list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.error_list.setContextMenuPolicy( Qt.CustomContextMenu )
        self.error_list.customContextMenuRequested.connect( self.show_context_menu )
        self.error_list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.combined_list.setContextMenuPolicy( Qt.CustomContextMenu )
        self.combined_list.customContextMenuRequested.connect(self.show_context_menu)
        self.combined_list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        # Connect button to execute code
        self.run_button.clicked.connect( self.run_code )

        # Set up window
        self.setWindowTitle('Executor 2.0')
        self.show()

        # Redirect stdout and stderr to custom widgets and the combined log
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        sys.stdout = OutputRedirector( self.output_list, self.combined_list, "-> " )
        sys.stderr = OutputRedirector( self.error_list, self.combined_list, "!> " )


    def get_current_cursor( self ):
        cursor = self.code_input.textCursor()
        return [ cursor.position(), cursor.blockNumber() + 1, cursor.columnNumber() + 1 ]

    def get_end_cursor( self ):
        cursor = self.code_input.textCursor()
        cursor.movePosition( QTextCursor.End )
        return [ cursor.position(), cursor.blockNumber() + 1, cursor.columnNumber() + 1 ]

    def set_end(self):
        ending = self.get_end_cursor()
        self.end_lc_label.setText( "End" )
        self.end_ch_label.setText( str(ending[1]) + "x" + str(ending[2] ) + ", " + str( ending[0] ) )

    def set_curr(self):
        current = self.get_current_cursor()
        self.cur_lc_label.setText( "Cursor" )
        self.cur_ch_label.setText( str(current[1]) + "x" + str(current[2] ) + ", " + str(current[0] ) )

    def clear_combined( self ):
        self.combined_list.clear()
    
    def custom_input(self, prompt=""):
        """Custom input function that will wait for input from the QLineEdit."""
        # Display the prompt in the QListWidget
        #fix 
        #self.console_output.addItem( "--> " + str( prompt ) )
        #self.console_output.scrollToBottom()

        # Show and enable the input line when input is needed
        self.input_line.show()
        self.run_button.hide()
        self.input_line.setEnabled(True)
        self.input_line.setFocus()
        self.waiting_for_input = True

        # Log the code to the combined widget with a prefix
        self.combined_list.addItem( "?> " + str( prompt ) )
        self.output_list.addItem( prompt )

        # Block execution until input is provided (this will wait until input_value is set)
        while self.waiting_for_input:
            QApplication.processEvents()  # Keep processing events to avoid freezing

        # Disable and hide input line after receiving input
        self.input_line.setEnabled(False)
        self.run_button.show()
        self.input_line.hide()
        #fix:
        #self.console_output.addItem( "<- " + str( self.input_value ) )

        # Return the value entered by the user
        self.output_list.addItem( "\"" + str( self.input_value ) + "\"" )
        self.combined_list.addItem( "<? \"" + str( self.input_value ) + "\"" )
        return self.input_value

    def submit_input(self):
        """Called when the user presses Enter in the QLineEdit."""
        if self.waiting_for_input:
            self.input_value = self.input_line.text()
            self.input_line.clear()
            self.waiting_for_input = False  # Resume code execution

    def run_code( self ):
        """
        Capture and execute the code from the QTextEdit, showing output/errors separately.
        Also logs the code to the combined widget.
        """
        # Clear previous output/errors
        self.output_list.clear()
        self.error_list.clear()

        # Get the code from the input box
        code = self.code_input.toPlainText()

        # Log the code to the combined widget with a prefix
        self.combined_list.addItem( "$> " + code )

        # Redirect stdout and stderr globally during code execution
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = OutputRedirector( self.output_list, self.combined_list, "-> " )
        sys.stderr = OutputRedirector( self.error_list, self.combined_list, "!> " )

        try:
            #exec( code, globals() )  # Replacing to redirect input
            #exec(code, {**globals(), "input": self.custom_input})
            exec(code, self.shared_namespace)
        except Exception as e:
            print(f"Error while executing code: {e}", file=sys.stderr)  # Capture exceptions in stderr
        finally:
            # Restore stdout and stderr after execution
            sys.stdout = old_stdout
            sys.stderr = old_stderr

    def show_context_menu( self, pos ):
        """
        Show a context menu to copy the selected item's text when right-clicked.
        """
        # Get the widget that triggered the context menu (output_list, error_list, or combined_list)
        sender_widget = self.sender()

        # Create the context menu
        menu = QMenu( self )

        # Add "Copy" option to the context menu
        copy_action = menu.addAction( "Copy" )

        # Execute the context menu
        action = menu.exec_( sender_widget.mapToGlobal( pos ) )

        # If the "Copy" option was selected and there is a selected item
        if action == copy_action:
            selected_item = sender_widget.currentItem()
            if selected_item:
                # Copy the text of the selected item to the clipboard
                clipboard = QApplication.clipboard()
                clipboard.setText( selected_item.text() )

    def closeEvent( self, event ):
        """
        Revert stdout and stderr to their original state when closing the window.
        """
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
        event.accept()




# This block only runs when the file is executed directly
if __name__ == '__main__':
    app = QApplication( sys.argv )
    window = CodeExecutorWindow()
    sys.exit( app.exec_() )


