
import sys, re, os
from PyQt5.QtWidgets import ( QApplication,  QTextEdit, QAction )
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt5.QtCore import Qt
from pygments import lex
from pygments import lexers # import LlvmLexer
from pygments.lexers import guess_lexer
from pygments.lexers import get_lexer_by_name
from pygments.token import Token
from pygments.styles.monokai import MonokaiStyle 
from pygments.styles import get_style_by_name

if __name__ == "__main__":
    from Executor import Executor
    from Testerwindow import testerwindow

def find_hex_color_code(input_string):
    hex_pattern = r"#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})\b"
    match = re.search(hex_pattern, input_string)
    if match:
        return match.group(0)
    return ""

class PythonHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for Python code using Pygments and Monokai style"""

    def __init__(self, document):
        super().__init__(document)
        self.lexer = lexers.PythonLexer()  
        # Apply Monokai style
        self.formatter = QSyntaxHighlighterFormatter(MonokaiStyle())  

    def highlightBlock(self, text):
        """Highlight each block of text using Pygments tokenization."""
        tokens = lex(text, self.lexer)
        index = 0

        for token_type, value in tokens:
            length = len(value)
            format = self.formatter.get_format(token_type)  # Get the QTextCharFormat for the token
            if format:
                self.setFormat(index, length, format)
            index += length
    def set_lexer( x ):
        self.lexer = x


class QSyntaxHighlighterFormatter:
    """Formatter that converts Pygments tokens to QTextCharFormat using Monokai style"""

    def __init__(self, pygments_style):
        self.style = pygments_style.styles
        self.formats = self._build_formats_from_style()

    def _build_formats_from_style(self):
        """Convert Pygments style definitions to PyQt formats."""
        formats = {}
        for token_type in self.style:
            text_format = QTextCharFormat()
            option_1 = find_hex_color_code( self.style[ token_type ] )
            if option_1 == "":
                try:
                    option_2 = find_hex_color_code( self.style[ token_type.split()[1] ] )
                    if option_2 == "":
                        color = '#ffffff'
                    else:
                        color = option_2
                except:
                    color = '#ffffff'
                    
            else:
                color = option_1
            qcolor = QColor( color ) 
            text_format.setForeground(qcolor)
            formats[token_type] = text_format
        return formats

    def get_format(self, token_type):
        """Return the QTextCharFormat for a given Pygments token type."""
        return self.formats.get( token_type, QTextCharFormat())  # Return default if not mapped


class editor_text_edit(QTextEdit):
    def __init__(self, parent=None):
        if not QApplication.instance():
            self.app = QApplication( sys.argv )
        super().__init__(parent)
        self.setPlaceholderText('Code here...')
        self.highlighter = PythonHighlighter(self.document())  # Apply highlighter
        #self.setStyleSheet("background-color:#000000")

        font = QFont( "Courier New" )
        font.setStyleHint( QFont.Monospace )  # Ensure monospaced style
        font.setPointSize(13)
        self.setFont( font )
        self.setAcceptRichText( False )
        self.setWindowTitle('Code_Window 2.0')
        #self.setWindowFlags(Qt.FramelessWindowHint)
        self.show()

        # Create context menu items
        self.increase_font_action = QAction( "Increase Font", self )
        self.decrease_font_action = QAction( "Decrease Font", self )

        # Connect actions to slots
        self.increase_font_action.triggered.connect( self.increase_font )
        self.decrease_font_action.triggered.connect( self.decrease_font )

        # Add actions to context menu
        self.setContextMenuPolicy( Qt.CustomContextMenu )
        self.customContextMenuRequested.connect( self.show_context_menu ) 

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab:
            # Insert 4 spaces instead of tab
            self.insertPlainText(" " * 4)
        else:
            # For other keys, default behavior
            super().keyPressEvent(event)

    def increase_font(self):
        font = self.font()
        new_size = font.pointSize() + 1

        font.setPointSize(new_size)
        self.setFont(font)

    def decrease_font(self):
        font = self.font()
        new_size = max(font.pointSize() - 1, 8)  # Ensure minimum font size

        font.setPointSize(new_size)
        self.setFont(font)

    def show_context_menu(self, point):
        menu = self.createStandardContextMenu()  # Get default context menu
        menu.addSeparator()
        menu.addAction(self.increase_font_action)
        menu.addAction(self.decrease_font_action)
        menu.exec_(self.mapToGlobal(point))

    def _set_monospaced_font( self, font ):
        if not font.styleHint() == QFont.Monospace:
            new_font = QFont( font.family(), font.pointSize() )
            new_font.setStyleHint( QFont.Monospace )
            font = new_font
        super().setFont( font )

    def set_bg_image( self, image ):
        first = """
        QTextEdit{
            background-repeat: no-repeat; 
            background-position: center;
            background-attachment: fixed;
            background-size: cover;
            background-image:url(""" 
        second = """) 0 0 0 0 stretch stretch;}"""
        self.setStyleSheet( first + image + second ) # self

if __name__ == '__main__':
    app = QApplication( sys.argv )

    editor0 = editor_text_edit()
    editor1 = editor_text_edit()
    editor2 = editor_text_edit()
    editor3 = editor_text_edit()
    editor4 = editor_text_edit()

    editor0.setWindowTitle('editor0 - Current windows')
    editor1.setWindowTitle('editor1 - Notes on Both')
    editor2.setWindowTitle('editor2 - Functions to Integrate')
    editor3.setWindowTitle('editor3 - Session Functions')
    editor4.setWindowTitle('editor4 - style.qss')

    images = [ "/home/jojo/Pictures/Slideshow WP/SpiderBebop.png",
              "/home/jojo/Pictures/Slideshow WP/Jrfw29Z (1).png" ]

    editor0.set_bg_image( images[0] )
    editor1.set_bg_image( images[0] )
    editor2.set_bg_image( images[0] )
    editor3.set_bg_image( images[0] )
    editor4.set_bg_image( images[0] )

    editor0.highlighter.lexer = lexers.PythonLexer()
    editor0.highlighter.rehighlight()
    editor1.highlighter.lexer = lexers.PythonLexer()
    editor1.highlighter.rehighlight()
    editor2.highlighter.lexer = lexers.PythonLexer()
    editor2.highlighter.rehighlight()
    editor3.highlighter.lexer = lexers.PythonLexer()
    editor3.highlighter.rehighlight()
    editor4.highlighter.lexer = lexers.CssLexer()
    editor4.highlighter.rehighlight()

    editor5 = editor_text_edit()
    filepath = os.path.expanduser('~/Desktop/Junkdrawer/Python/CrapTestic/sample4.py')
    with open( filepath, "r" ) as file:
        editor5.setText( file.read() )

    editor5.set_bg_image( images[0] )
    editor5.setWindowTitle('editor5 - ' + str( os.path.basename( filepath ) ) )

    editor0.activateWindow()

    button_window = testerwindow()
    button_window.add_button( lambda: editor0.activateWindow(), "Show editor0" )
    button_window.add_button( lambda: editor1.activateWindow(), "Show editor1" )
    button_window.add_button( lambda: editor2.activateWindow(), "Show editor2" )
    button_window.add_button( lambda: editor3.activateWindow(), "Show editor3" )
    button_window.add_button( lambda: editor4.activateWindow(), "Show editor4" )
    button_window.add_button( lambda: editor5.activateWindow(), "Show editor5" )
    button_window.add_text_line( "line1" )
    button_window.add_text_block( "block1" )
    button_window.setWindowFlags( button_window.windowFlags() | Qt.WindowStaysOnTopHint )
    button_window.set_new_stylesheet()
    button_window.show()
    
    Executor_Window = Executor() # you cannot reference the above windows above from Executor when done this way

    sys.exit( app.exec_() )