import sys, re, os
from PyQt5.QtWidgets import ( QApplication,  QTextEdit, QAction,QVBoxLayout,QWidget,QLabel,QPushButton, QToolButton )
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont, QIcon, QPixmap, QPainter, QPainterPath, QRegion
from PyQt5.QtCore import Qt, QByteArray, QSize, QEvent
from Editor.EditorTE import editor_text_edit
from PyQt5.QtSvg import QSvgRenderer

svg_minus = '''<svg width="40" height="40" xmlns="http://www.w3.org/2000/svg">
   <circle cx="20" cy="20" r="18" stroke="#330033" stroke-width="4" fill="#990077" />
   <line x1=10 y1= 20 x2=30 y2=20 stroke="#330033" stroke-width="4" /> 
</svg> '''

min_svg = '''<svg height="20" width="20">
  <circle r="9" cx="10" cy="10" style="fill:gold;stroke:white;stroke-width:0" />  
  <line x1="6" y1="10" x2="14" y2="10" style="fill:black;stroke:black;stroke-width:3" />
</svg>'''

svg_plus = '''<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
   <circle cx="50" cy="50" r="40" stroke="#330033" stroke-width="4" fill="#990077" />
   <line x1=20 y1= 50 x2=80 y2=50 stroke="#330033" stroke-width="4" /> 
   <line x1=50 y1= 20 x2=50 y2=80 stroke="#330033" stroke-width="4" /> 
</svg> '''

class editor( QWidget ):
    def __init__( self ):
        if not QApplication.instance():
            self.app = QApplication( sys.argv )
        super().__init__()
        self.editor_text_edit = editor_text_edit()
        self.editor_layout = QVBoxLayout( self )
        self.editor_layout.setContentsMargins(0,0,0,0)        
        self.top_widget()
        self.editor_layout.addWidget( self.editor_text_edit )
        self.editor_layout.setStyleSheet()
        self.bottom_widget()
        self.setContentsMargins(0,0,0,0)
        self.setWindowFlags( self.windowFlags() | Qt.WindowStaysOnTopHint )
        self.show()
        
    def top_widget( self ): 
        self.top_widget = QWidget()
        editor9.top_widget.setStyleSheet("background-color: gray;" )
        self.top_layout = QVBoxLayout( self.top_widget )
        self.pin = QToolButton( self )
        pinned_icon = self.create_icon_from_svg( min_svg )
        self.pin.setFixedSize(QSize( 20, 20))
        self.pin.setIcon( QIcon( pinned_icon ) )
        #self.save_button = QToolButton()
        #self.pin = QToolButton()
        #self.pin = QToolButton()
        self.pin.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.pin.setFixedSize(QSize( 40, 40))
        self.pin.clicked.connect( self.top_widget.hide )
        #self.pin.setStyleSheet()
        self.top_layout.addWidget( self.pin )
        #self.top_widget.addLayout( self.top_layout )
        self.editor_layout.addWidget( self.top_widget )
        self.top_widget.setContentsMargins(0,0,0,0)
        self.top_layout.setContentsMargins(0,0,0,0)

    def bottom_widget( self ):
        # No, I don't want to use QMainWindow:MenuBar/Statusbar
        self.bottom_widget = QWidget()
        self.label_box = QHBoxLayout( self.bottom_widget )
        self.cur_lc_label  = QLabel( "Cursor" )
        self.cur_lc_label.setAlignment( Qt.AlignLeft )
        self.label_box.addWidget( self.cur_lc_label )
        
        self.cur_ch_label = QLabel( "0x0, 0" )
        self.cur_ch_label.setAlignment(Qt.AlignCenter)
        self.label_box.addWidget( self.cur_ch_label )
        
        self.end_lc_label = QLabel( "End" )
        self.end_lc_label.setAlignment(Qt.AlignCenter)
        self.label_box.addWidget( self.end_lc_label )
        
        self.end_ch_label = QLabel( "0x0, 0" )
        self.end_ch_label.setAlignment(Qt.AlignRight)
        self.label_box.addWidget( self.end_ch_label )
        self.editor_layout.addWidget( self.bottom_widget )
        self.bottom_widget.setContentsMargins(0,0,0,0)
        self.label_box.setContentsMargins(0,0,0,0)
        # Set code for labels:
        self.editor_text_edit.cursorPositionChanged.connect( self.set_curr )
        self.editor_text_edit.textChanged.connect( self.set_end )
        self.editor_text_edit.installEventFilter(self)
        
    def eventFilter( self, obj, event ):
        # Check if the event is a context menu request from the custom text edit
        if obj == self.editor_text_edit and event.type() == QEvent.ContextMenu:
            self.extend_context_menu(event)
            return True  # Event has been handled
        print(event)
        return super().eventFilter(obj, event)

    def extend_context_menu( self, event ):
        # Get the existing custom context menu from the QTextEdit
        context_menu = self.editor_text_edit.createStandardContextMenu()

        # Add custom actions to the context menu
        custom_action = QAction( "Show Toolbar", self )
        custom_action.triggered.connect( self.top_widget.show )
        context_menu.addAction(custom_action)

        # Show the context menu at the cursor's position
        context_menu.exec_(event.globalPos())

    def get_current_cursor( self ):
        cursor = self.editor_text_edit.textCursor()
        return [ cursor.position(), cursor.blockNumber() + 1, cursor.columnNumber() + 1 ]

    def get_end_cursor( self ):
        cursor = self.editor_text_edit.textCursor()
        cursor.movePosition( QTextCursor.End )
        return [ cursor.position(), cursor.blockNumber() + 1, cursor.columnNumber() + 1 ]

    def set_end( self ):
        ending = self.get_end_cursor()
        self.end_lc_label.setText( "End" )
        self.end_ch_label.setText( str(ending[1]) + "x" + str(ending[2] ) + ", " + str( ending[0] ) )

    def set_curr( self ):
        current = self.get_current_cursor()
        self.cur_lc_label.setText( "Cursor" )
        self.cur_ch_label.setText( str(current[1]) + "x" + str(current[2] ) + ", " + str(current[0] ) )

    def create_icon_from_svg( self, svg_data ):
        svg_byte_array = QByteArray(svg_data.encode( 'utf-8' ) )
        svg_renderer = QSvgRenderer( svg_byte_array )
        pixmap = QPixmap( svg_renderer.defaultSize() )
        pixmap.fill( Qt.transparent )  # Transparent background
        painter = QPainter( pixmap )
        svg_renderer.render( painter )
        painter.end()
        return pixmap

if __name__ == '__main__':
    editor9 = editor()
    editor9.setWindowTitle( "Editor 9" )
   