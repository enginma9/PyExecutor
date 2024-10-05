from PyQt5.QtWidgets import ( QWidget, QApplication, QToolButton, QPushButton,
    QVBoxLayout, QDialog, QMenu, QLineEdit, QScrollArea
)
from PyQt5.QtCore import Qt
from CustomText import CustomTextEdit
import sys

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
    
    """
    
    def __init__(self, args=None):
        """
        Initializes the testerwindow, creates a QApplication if needed, and sets up the layout.
        
        """
        if not QApplication.instance():
            self.app = QApplication( sys.argv )
        super().__init__()
        self.item_dict = {}  # To hold references to items created

        self.main_layout = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.widget_x = QWidget()
        self.layout = QVBoxLayout()

        self.scroll_area.setWidgetResizable( True )
        self.layout.addStretch()

        self.setLayout( self.main_layout )
        self.main_layout.addWidget( self.scroll_area )
        self.scroll_area.setWidget(self.widget_x)
        self.widget_x.setLayout( self.layout )

        #setContentsMargins(left, top, right, bottom)
        self.setContentsMargins( 0,0,0,0 )
        self.setGeometry(100, 100, 400, 500)
        self.setWindowTitle( 'Tester Window' )
        self.setObjectName('testerwindow')
        self.show()
        
    def add_button(self, function_to_be_called=None, text=None):
        """
        Adds a button to the window. If the button text is already in use, the existing button is deleted before adding a new one.
        
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
        #self.layout.insertWidget( self.layout.count() - 1, button )
        self.item_dict[ text ] = button

    def set_new_stylesheet( self, styleFile="style.qss" ):
        with open(styleFile, "r") as fh: 
            self.setStyleSheet(fh.read())

    def add_text_line( self, title=None, label=None ):
        """
        Adds a text input line (QLineEdit) to the window. Optionally, a label can be added.

        """
        if title is None:
            title = f"TextLine { len( self.item_dict ) + 1 }"
        line_edit = QLineEdit( self )
        line_edit.setPlaceholderText(title)
        if label:
            label_widget = QLabel( label, self )
            self.layout.addWidget( label_widget )
        self.layout.addWidget( line_edit )

        # Store reference in item_dict
        self.item_dict[ title ] = line_edit

    def add_text_block( self, title=None ):
        """
        Adds a text block ( QTextEdit ) to the window.
        
        """
        if title is None:
            title = f"TextBlock { len( self.item_dict ) + 1 }"
        text_edit = CustomTextEdit( self )
        text_edit.setPlaceholderText( title )
        text_edit.setMinimumHeight( 250 )
        self.layout.addWidget( text_edit )

        # Store reference in item_dict
        self.item_dict[ title ] = text_edit
        self.item_dict[ title ].setPlaceholderText( title )

    def get_text_from( self, input_field_name ):
        """
        Returns the text from the specified input field.
        
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
        
        """
        if input_field_name in self.item_dict:
            print( "moving to:", input_field_name )
            widget = self.item_dict[ input_field_name ]
            widget.setText( text )

    def exec( self ):
        """
        Starts the Qt event loop. This must be called after setting up the window.
        
        """
        return self.app.exec_()

    def __del__( self ):
        """
        Destructor to clean up and exit the application when the window is closed.
        """
        print( "Cleaning up and exiting the application." )
        sys.exit(0)

