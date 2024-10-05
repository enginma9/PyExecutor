import sys, io

def import_modules():
    # Qt Modules
    import_module( "PyQt5.QtWidgets", fromlist=[ 
        "QApplication", "QWidget", "QVBoxLayout", "QHBoxLayout", "QTabWidget",
        "QPushButton", "QLineEdit", "QLabel", "QTextEdit", "QListWidget", 
        "QPlainTextEdit", "QAction", "QAbstractItemView", "QDialog", "QMenu",
        "QSplitter"
    ] )
    import_module( "PyQt5.QtGui", fromlist=[ "QClipboard","QFont","QCursor", "QTextCursor" ] )
    import_module( "PyQt5.QtCore", fromlist=[ "Qt" ] )
    # This project
    import_module( "OutputRedirect", fromlist=[ "OutputRedirector" ] )
    import_module( "Helpers.Helpers", fromlist=[ "get_globals", "print_attributes", "print_keys", "print_nested", "get_nested_keys" ] )
    import_module( "CustomText", fromlist=[ "CustomTextEdit" ] )
    import_module( "Testerwindow", fromlist=["testerwindow"] )

def import_module(modulename, shortname=None, asfunction=False, fromlist=None):
    # Only using this on top-level module rather than having every import in the project in globals()
    if shortname is None:
        shortname = modulename
    
    if asfunction is False:
        if fromlist:
            # Handle sub-item imports like "from PyQt5.QtWidgets import QApplication"
            module = __import__(modulename, fromlist=fromlist)
            for item in fromlist:
                globals()[item] = getattr(module, item)
        else:
            # Simple import case
            globals()[shortname] = __import__(modulename)
    else:
        # Handle function or specific item import like "from X import Y"
        module = __import__(modulename, fromlist=[shortname])
        globals()[shortname] = getattr(module, shortname)

import_modules()
#print("Imports successful.")

class Executor( QWidget ):
    def __init__( self ):
        if not QApplication.instance():
            self.app = QApplication( sys.argv )
        super().__init__()

        self.shared_namespace = globals()
        self.layout = QVBoxLayout( self )
        self.set_style()
        self.build_top() # 
        self.build_labels() # creates label_box, builds all labels and places
        self.build_bottom()

        self.run_button.clicked.connect( self.run_code )

        # Set up window
        self.setWindowTitle('Executor 2.0')
        self.show()
        self.redirect()
        
    def set_style( self ):
        self.setObjectName('Executor')
        # Set Style
        try:
            styleFile = "style.qss" 
            with open(styleFile, "r") as fh: 
                self.setStyleSheet(fh.read())
        except:
            pass

    def build_top( self ): # 
        # Top
        # Text box for user to input Python code
        self.code_input = CustomTextEdit( self )
        self.layout.addWidget( self.code_input )

        # Button to execute the Python code
        self.run_button = QPushButton( "Run Code", self )
        self.layout.addWidget( self.run_button )
        
        # Hidden Input
        self.input_line = QLineEdit(self)
        self.input_line.setPlaceholderText("Input")
        self.input_line.setEnabled(False)  # Disabled until input() is called
        self.layout.addWidget(self.input_line)
        self.input_line.hide()

        # Connect Enter key to simulate input
        self.input_line.returnPressed.connect( self.submit_input )

        self.shared_namespace.update({"input": self.custom_input})
        
    def build_labels( self ): # creates label_box, builds all labels and places# Mid
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

    def build_bottom( self ):
        # Create a tab widget
        self.tab_widget = QTabWidget( self )
        self.layout.addWidget( self.tab_widget )

        self.build_first_tab()
        self.build_second_tab()
        # place

    def build_first_tab( self ):
        # First tab for output and error lists
        self.output_error_tab = QWidget()
        self.output_error_layout = QVBoxLayout( self.output_error_tab )
        self.std_split = QSplitter(Qt.Vertical)
        # Add tab to tab widget
        self.tab_widget.addTab( self.output_error_tab, "stdout/stderr" )
        
        # List widgets for output and errors
        self.output_list = QListWidget( self )
        self.error_list = QListWidget( self )
        # Style
        self.output_list.setAlternatingRowColors( True )
        self.error_list.setAlternatingRowColors( True )
        # Place
        self.std_split.addWidget( self.output_list )
        self.std_split.addWidget( self.error_list )
        self.output_error_layout.addWidget( self.std_split )
        # Enable context menu
        #self.output_list.setContextMenuPolicy( Qt.CustomContextMenu )
        #self.output_list.customContextMenuRequested.connect( self.show_context_menu )
        #self.output_list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        
        self.set_list_properties( self.output_list )

        self.error_list.setContextMenuPolicy( Qt.CustomContextMenu )
        self.error_list.customContextMenuRequested.connect( self.show_context_menu )
        self.error_list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
    
    def build_second_tab( self ):
        # Second tab for combined log
        self.combined_tab = QWidget()
        self.combined_layout = QVBoxLayout( self.combined_tab )
        # Add tab to tab widget
        self.tab_widget.addTab( self.combined_tab, "Log" )

        # Combined list widget in the second tab
        self.combined_list = QListWidget( self )
        self.combined_list.setAlternatingRowColors( True )
        self.combined_layout.addWidget( self.combined_list )

        # Enable context menu
        self.combined_list.setContextMenuPolicy( Qt.CustomContextMenu )
        self.combined_list.customContextMenuRequested.connect(self.show_context_menu)
        self.combined_list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.clr_comb_button = QPushButton( "Clear", self )
        self.combined_layout.addWidget( self.clr_comb_button )
        self.clr_comb_button.clicked.connect( self.clear_combined )
    
    def set_list_properties( self, list_widget ):
        list_widget.setContextMenuPolicy( Qt.CustomContextMenu )
        list_widget.customContextMenuRequested.connect( self.show_context_menu )
        list_widget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

    def redirect( self ):
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
        #\"""Custom input function that will wait for input from the QLineEdit.\"""
        # Display the prompt in the QListWidget
        #print("custom_input")
        self.output_list.addItem( "" + str( prompt ) )
        self.input_line.setPlaceholderText( prompt )
        self.output_list.scrollToBottom()

        # Show and enable the input line when input is needed
        self.input_line.show()
        self.run_button.hide()
        self.input_line.setEnabled(True)
        self.input_line.setFocus()
        self.waiting_for_input = True

        # Log the code to the combined widget with a prefix
        self.combined_list.addItem( "?> " + str( prompt ) )
        #self.output_list.addItem( prompt )

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
        #\"""Called when the user presses Enter in the QLineEdit.\"""
        #print("submit_input")
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
        self.output_list.clear()    #
        self.error_list.clear()     #

        # Get the code from the input box
        code = self.code_input.toPlainText()    #

        # Log the code to the combined widget with a prefix
        self.combined_list.addItem( "$> " + code )

        # Redirect stdout and stderr globally during code execution
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = OutputRedirector( self.output_list, self.combined_list, "-> " )
        sys.stderr = OutputRedirector( self.error_list, self.combined_list, "!> " )

        try:
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


if __name__ == '__main__':
    app = QApplication( sys.argv )
    window = Executor()
    sys.exit( app.exec_() )


