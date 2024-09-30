from PyQt5.QtWidgets import ( QWidget, QApplication, QToolButton, QPushButton,
    QVBoxLayout, QDialog, QMenu, QLineEdit, QScrollArea
)
from CustomText import CustomTextEdit


class testerwindow( QWidget ):
    """
    A class to create a simple window for testing buttons, text inputs, and text blocks.
    
    Attributes:
    ----------
    item_dict : dict
        A dictionary holding references to created buttons, text lines, and text blocks.
    
    Methods:
    -------
    add_button(function_to_be_called=None, text=None):
        Adds a button with the specified function and text.
        
    add_text_line(title=None, label=None):
        Adds a text line (QLineEdit) with an optional title and label.
        
    add_text_block(title=None):
        Adds a text block (QPlainTextEdit) with an optional title.
        
    get_text_from(input_field_name):
        Returns the text from the specified input field by name.

    show_keyboard_lsnr():
        Un-hides the keyboard listener layout.
        
    hide_keyboard_lsnr():
        Hides the keyboard listener layout.
        
    exec():
        Starts the Qt application event loop.
    
    Example syntax:
        from qtfunctester import testerwindow
        
        # Create object and window
        the_window = testerwindow()

        #Create QTextEdit, or text block
        the_window.add_text_block( "Example" )

        # Create button, set to print whatever is in the text block
        the_window.add_button( lambda: print( the_window.get_text_from( "Example" ) ), "Custom Button" )
        
        # You can put spaces in the button name, because the string matches up, in item_dict, to the object
        the_window.add_text_block( "Text Two" )
        the_window.add_button(lambda: print( the_window.get_text_from("Text Two") ), "Print from 'Poo pie'")

        # You can use this in Python console.  If you alter a function after creating a button that calls it,
        #  it will still call the function without issue... unless you do something like change the number of 
        #  parameters or something else Python won't like in your code.
        
        

    """
    
    def __init__(self, args=None):
        """
        Initializes the testerwindow, creates a QApplication if needed, and sets up the layout.
        
        If `args` is a list of tuples, buttons are added based on the tuples.
        
        Parameters:
        ----------
        args : list of tuples, optional
            A list of (text, function) tuples to add buttons automatically.
        """
        if not QApplication.instance():
            self.app = QApplication( sys.argv )

        super().__init__()
        scroll_area = QScrollArea()
        self.item_dict = {}  # To hold references to items created
        self.layout = QVBoxLayout( self )  # Main layout for the window
        self.listener_layout = None  # Layout for the keyboard listener
        self.print_key = False  # Toggle flag for listener
        #self.create_keyboard_lsnr()  # Call keyboard listener creation

        # If args is a list of tuples, add buttons for each tuple
        if args and isinstance( args, list ):
            for text, function in args:
                self.add_button( function, text )

        self.setWindowTitle( 'Tester Window' )
        self.show()
        #self.hide_keyboard_lsnr()

    def add_button(self, function_to_be_called=None, text=None):
        """
        Adds a button to the window. If the button text is already in use, the existing button is deleted before adding a new one.
        
        Parameters:
        ----------
        function_to_be_called : callable, optional
            The function to be called when the button is clicked.
        
        text : str, optional
            The text to display on the button. If not provided, a default name is generated.
        """
        if text is None:
            text = f"Button { len( self.item_dict ) + 1 }"
        
        # Check if the button text already exists and remove it if it does
        if text in self.item_dict:
            old_button = self.item_dict.pop( text )
            old_button.deleteLater()  # Remove the existing button
        
        # Create the new button
        button = QPushButton( text, self )
        if function_to_be_called:
            button.clicked.connect( function_to_be_called )
        
        # Add to layout and store reference in item_dict
        self.layout.addWidget( button )
        self.item_dict[ text ] = button

    def set_new_stylesheet( self, styleFile="style.qss" ):
        with open(styleFile, "r") as fh: 
            self.setStyleSheet(fh.read())

    def add_text_line( self, title=None, label=None ):
        """
        Adds a text input line (QLineEdit) to the window. Optionally, a label can be added.
        
        Parameters:
        ----------
        title : str, optional
            The name to identify the input field. If not provided, a default title is generated.
        
        label : str, optional
            The text to display as a label above the input field.
        """
        if title is None:
            title = f"TextLine { len( self.item_dict ) + 1 }"
        line_edit = QLineEdit( self )
        if label:
            label_widget = QLabel( label, self )
            self.layout.addWidget( label_widget )
        self.layout.addWidget( line_edit )

        # Store reference in item_dict
        self.item_dict[ title ] = line_edit

    def add_text_block( self, title=None ):
        """
        Adds a text block ( QTextEdit ) to the window.
        
        Parameters:
        ----------
        title : str, optional
            The name to identify the text block. If not provided, a default title is generated.
        """
        if title is None:
            title = f"TextBlock { len( self.item_dict ) + 1 }"
        text_edit = CustomTextEdit( self )
        self.layout.addWidget( text_edit )

        # Store reference in item_dict
        self.item_dict[ title ] = text_edit

    def get_text_from( self, input_field_name ):
        """
        Returns the text from the specified input field.
        
        Parameters:
        ----------
        input_field_name : str
            The name of the input field to retrieve text from.
        
        Returns:
        -------
        str or None
            The text from the input field, or None if the field doesn't exist.
        """
        if input_field_name in self.item_dict:
            widget = self.item_dict[ input_field_name ]
            if isinstance( widget, QLineEdit ):
                return widget.text()
            elif isinstance( widget, CustomTextEdit ):
                return widget.toPlainText()
        return None

    def set_text_in( self, input_field_name, text ):
        """
        Sets the text from the specified input field.
        
        Parameters:
        ----------
        input_field_name : str
            The name of the input field to retrieve text from.
        text
            String to put in given input field

        Returns:
        -------
        None
        
        """
        if input_field_name in self.item_dict:
            widget = self.item_dict[ input_field_name ]

    def exec( self ):
        """
        Starts the Qt event loop. This must be called after setting up the window.
        
        Returns:
        -------
        int
            The exit status of the application.
        """
        return self.app.exec_()

    def __del__( self ):
        """
        Destructor to clean up and exit the application when the window is closed.
        """
        print( "Cleaning up and exiting the application." )
        sys.exit(0)

