import sys
from PyQt5.QtWidgets import ( QApplication,  QTextEdit, QAction )
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt5.QtCore import Qt
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.token import Token
from pygments.styles.monokai import MonokaiStyle

class PythonHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for Python code using Pygments and Monokai style"""

    def __init__(self, document):
        super().__init__(document)
        self.lexer = PythonLexer()  # Use PythonLexer from Pygments
        self.formatter = QSyntaxHighlighterFormatter(MonokaiStyle())  # Apply Monokai style

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
            if self.style[token_type] == "":
                top_tokin = token_type.split()[1]
                if self.style[top_tokin] == "":
                    color = '#ffffff'
                else:
                    color = self.style[top_tokin]
            else:
                color = self.style[token_type]
            #print( token_type, color )
            qcolor = QColor( color ) 
            text_format.setForeground(qcolor)
            formats[token_type] = text_format
        return formats

    def get_format(self, token_type):
        """Return the QTextCharFormat for a given Pygments token type."""
        return self.formats.get( token_type, QTextCharFormat())  # Return default if not mapped


class CustomTextEdit(QTextEdit):
    def __init__(self, parent=None):
        if not QApplication.instance():
            self.app = QApplication( sys.argv )
        super().__init__(parent)
        self.setPlaceholderText('Start typing Python code here...')
        self.highlighter = PythonHighlighter(self.document())  # Apply highlighter

        font = QFont( "Courier New" )
        font.setStyleHint( QFont.Monospace )  # Ensure monospaced style
        font.setPointSize(13)
        self.setFont( font )

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
            # If the font is not monospaced, create a new monospaced font with the same point size
            new_font = QFont( font.family(), font.pointSize() )
            new_font.setStyleHint( QFont.Monospace )
            font = new_font
        super().setFont( font )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = CustomTextEdit()
    editor.show()
    sys.exit(app.exec_())
