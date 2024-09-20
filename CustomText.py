from PyQt5.QtWidgets import ( QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLineEdit, QLabel, QTextEdit, QListWidget, QTabWidget, QMenu, 
    QPlainTextEdit, QAction, QAbstractItemView )
from PyQt5.QtGui import QClipboard, QFont
from PyQt5.QtCore import Qt

import sys
import io



class CustomTextEdit( QTextEdit ):
    def __init__( self, parent=None ):
        if not QApplication.instance():
            self.app = QApplication( sys.argv )
        super().__init__( parent )

        # Set the default font to a monospaced font (e.g., Courier New)
        font = QFont( "Courier New" )
        font.setStyleHint( QFont.Monospace )  # Ensure monospaced style
        font.setPointSize(13)
        self.setFont( font )

        # Override the font property to enforce monospaced fonts
        self.setFont = self._set_monospaced_font

        # Override the color property to prevent color changes
        self.setTextColor = self._prevent_color_change
        self.setAcceptRichText( False )


        # Create context menu items
        self.increase_font_action = QAction( "Increase Font", self )
        self.decrease_font_action = QAction( "Decrease Font", self )

        # Connect actions to slots
        self.increase_font_action.triggered.connect( self.increase_font )
        self.decrease_font_action.triggered.connect( self.decrease_font )

        # Add actions to context menu
        self.setContextMenuPolicy( Qt.CustomContextMenu )
        self.customContextMenuRequested.connect( self.show_context_menu ) 
        #self.textChanged.connect

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

    def _prevent_color_change( self, color ):
        # Ignore color changes
        pass

    def keyPressEvent( self, event ):
        if event.key() == 0x01000001:  # Qt.Key_Tab
            cursor = self.textCursor()
            cursor.insertText('    ')  # Insert 4 spaces
        else:
            super().keyPressEvent( event )  # Process other keys normally
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    CT = CustomTextEdit()
    CT.show()
    sys.exit(app.exec())
