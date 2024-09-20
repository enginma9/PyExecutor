# Only got this truly working on Kubuntu, 
# probably works in Ubuntu, but did not test, 
# Windows - can not drag window around screen, 
# Lubuntu - no dragging, and qss not entirely respected.  
# Had some issues that were related to installed packages, but I don't believe that was the reason here. 

# Import PyQt resources
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (
    QApplication, QHBoxLayout, QLabel, QMainWindow, QVBoxLayout, QWidget,
    QToolButton, QPushButton, QListWidget, QTabWidget, QAbstractItemView, QMenu
)
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPainterPath, QRegion
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import QByteArray, QEvent
from PyQt5 import QtCore, QtGui, QtWidgets
# Other Libraries
import sys
import io
# This project 
from CustomText import CustomTextEdit
from Helpers import get_globals, print_attributes, print_keys, print_nested, get_nested_keys
from CustomText import CustomTextEdit
from Testerwindow import testerwindow
from OutputRedirect import OutputRedirector

min_svg = '''<svg height="20" width="20">
  <circle r="9" cx="10" cy="10" style="fill:gold;stroke:white;stroke-width:0" />  
  <line x1="6" y1="10" x2="14" y2="10" style="fill:black;stroke:black;stroke-width:3" />
</svg>'''

max_svg = '''<svg height="20" width="20" xmlns="http://www.w3.org/2000/svg">
  <circle r="9" cx="10" cy="10" style="fill:lime;stroke:white;stroke-width:0" />    
  <polygon points="10,5 14,13 6,13" style="fill:black;stroke:black;stroke-width:0" />
</svg>'''

normal_svg = '''<svg height="20" width="20" xmlns="http://www.w3.org/2000/svg">
  <circle r="9" cx="10" cy="10" style="fill:lime;stroke:white;stroke-width:0" />    
  <polygon points="10,15 14,7 6,7" style="fill:black;stroke:black;stroke-width:0" />
</svg>'''

close_svg = '''<svg height="20" width="20">
  <circle r="9" cx="10" cy="10" style="fill:MediumVioletRed;stroke:white;stroke-width:0" /> 
  <line x1="7" y1="7" x2="13" y2="13" style="fill:black;stroke:black;stroke-width:3" />
  <line x1="7" y1="13" x2="13" y2="7" style="fill:black;stroke:black;stroke-width:3" />  
</svg>''' 


class SideGrip(QtWidgets.QWidget):
    def __init__(self, parent, edge):
        super().__init__(parent)
        if edge == QtCore.Qt.LeftEdge:
            self.setCursor(QtCore.Qt.SizeHorCursor)
            self.resizeFunc = self.resizeLeft
        elif edge == QtCore.Qt.TopEdge:
            self.setCursor(QtCore.Qt.SizeVerCursor)
            self.resizeFunc = self.resizeTop
        elif edge == QtCore.Qt.RightEdge:
            self.setCursor(QtCore.Qt.SizeHorCursor)
            self.resizeFunc = self.resizeRight
        else:
            self.setCursor(QtCore.Qt.SizeVerCursor)
            self.resizeFunc = self.resizeBottom
        self.mousePos = None
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def resizeLeft(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() - delta.x())
        geo = window.geometry()
        geo.setLeft(geo.right() - width)
        window.setGeometry(geo)

    def resizeTop(self, delta):
        window = self.window()
        height = max(window.minimumHeight(), window.height() - delta.y())
        geo = window.geometry()
        geo.setTop(geo.bottom() - height)
        window.setGeometry(geo)

    def resizeRight(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() + delta.x())
        window.resize(width, window.height())

    def resizeBottom(self, delta):
        window = self.window()
        height = max(window.minimumHeight(), window.height() + delta.y())
        window.resize(window.width(), height)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mousePos = event.pos()

    def mouseMoveEvent(self, event):
        if self.mousePos is not None:
            delta = event.pos() - self.mousePos
            self.resizeFunc(delta)

    def mouseReleaseEvent(self, event):
        self.mousePos = None
        

class frameless_exec_win(QtWidgets.QMainWindow):
    _gripSize = 8  # Size of the grips
    def __init__(self):
        super().__init__()
        # Style       
        with open( "style.qss", "r" ) as fh: 
            self.setStyleSheet( fh.read() )
        self.setWindowTitle("Mojo's  Multi-line Live Editor ")
        
        #self.resize(400, 300)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.title_bar = CustomTitleBar(self)

        # Set the central widget
        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setObjectName("Container")
        self.central_widget.setStyleSheet("""
            #Container {
                background: qlineargradient(x1:0 y1:0, x2:1 y2:1, stop:0 #051c2a stop:1 #44315f);
                border-radius: 5px;
            }
        """)

        # Layout for window content
        self.work_space_layout = QtWidgets.QVBoxLayout()
        self.work_space_layout.setContentsMargins(11, 11, 11, 0)
        self.code_input = CustomTextEdit() #QtWidgets.QPlainTextEdit()
        self.work_space_layout.addWidget(self.code_input)
        self.run_button = QtWidgets.QPushButton("Run It")
        #self.run_button.clicked.connect( self.stylin )
        self.work_space_layout.addWidget(self.run_button)
        
        self.word_space_layout = QtWidgets.QHBoxLayout()
        self.word_l_label = QLabel( "One" )
        self.word_r_label = QLabel( "Two" )

        self.word_r_label.setAlignment( Qt.AlignRight )

        self.word_space_layout.addWidget( self.word_l_label )
        self.word_space_layout.addWidget( self.word_r_label )
        self.work_space_layout.addLayout( self.word_space_layout )

        # Create a tab widget
        self.tab_widget = QTabWidget( self )
        self.work_space_layout.addWidget( self.tab_widget )

        # First tab for output and error lists
        self.output_error_tab = QWidget()
        self.output_error_layout = QVBoxLayout( self.output_error_tab )

        # Second tab for combined log
        self.combined_tab = QWidget()
        self.combined_layout = QVBoxLayout( self.combined_tab )

        # Add tabs to the tab widget
        self.tab_widget.addTab( self.output_error_tab, "stdout/stderr" )
        self.tab_widget.addTab( self.combined_tab, "Log" )

        # List widgets for output and errors in the first tab
        self.output_list = QListWidget( self )
        self.error_list = QListWidget( self )
        # Style
        self.output_list.setAlternatingRowColors( True )
        self.error_list.setAlternatingRowColors( True )
        # Place
        self.output_error_layout.addWidget( self.output_list )
        self.output_error_layout.addWidget( self.error_list )

        # Combined list widget in the second tab
        self.combined_list = QListWidget( self )
        self.combined_list.setAlternatingRowColors( True )
        self.combined_layout.addWidget( self.combined_list )
        self.clr_comb_button = QPushButton( "Clear", self )
        self.combined_layout.addWidget( self.clr_comb_button )
        self.clr_comb_button.clicked.connect( self.clear_combined )

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

        # Main layout for the central widget
        central_widget_layout = QtWidgets.QVBoxLayout()
        central_widget_layout.setContentsMargins(0, 0, 0, 10)
        central_widget_layout.setAlignment(QtCore.Qt.AlignTop)

        # Add the custom title bar, menu bar, toolbar, and workspace in correct order
        central_widget_layout.addWidget(self.title_bar)  # Custom title bar at the top
        central_widget_layout.addLayout(self.work_space_layout)  # Workspace content below

        self.central_widget.setLayout(central_widget_layout)
        self.setCentralWidget(self.central_widget)

        # Add side grips for resizing
        self.sideGrips = [
            SideGrip(self, QtCore.Qt.LeftEdge), 
            SideGrip(self, QtCore.Qt.TopEdge), 
            SideGrip(self, QtCore.Qt.RightEdge), 
            SideGrip(self, QtCore.Qt.BottomEdge), 
        ]
        self.cornerGrips = [QtWidgets.QSizeGrip(self) for i in range(4)]
        for grip in self.sideGrips:
            grip.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Initialize the grips and round the corners
        self.updateGrips()
        self.round_corners()

        # Redirect stdout and stderr to custom widgets and the combined log
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        sys.stdout = OutputRedirector( self.output_list, self.combined_list, "-> " )
        sys.stderr = OutputRedirector( self.error_list, self.combined_list, "!> " )

    @property
    def gripSize(self):
        return self._gripSize

    def setGripSize(self, size):
        if size == self._gripSize:
            return
        self._gripSize = max(2, size)
        self.updateGrips()

    def updateGrips(self):
        """Update the size and position of the side and corner grips."""
        self.setContentsMargins(self.gripSize, self.gripSize, self.gripSize, self.gripSize)

        outRect = self.rect()
        # an "inner" rect used for reference to set the geometries of size grips
        inRect = outRect.adjusted(self.gripSize, self.gripSize, -self.gripSize, -self.gripSize)

        # Top-left corner
        self.cornerGrips[0].setGeometry(QtCore.QRect(outRect.topLeft(), inRect.topLeft()))
        # Top-right corner
        self.cornerGrips[1].setGeometry(QtCore.QRect(outRect.topRight(), inRect.topRight()).normalized())
        # Bottom-right corner
        self.cornerGrips[2].setGeometry(QtCore.QRect(inRect.bottomRight(), outRect.bottomRight()))
        # Bottom-left corner
        self.cornerGrips[3].setGeometry(QtCore.QRect(outRect.bottomLeft(), inRect.bottomLeft()).normalized())

        # Left edge
        self.sideGrips[0].setGeometry(0, inRect.top(), self.gripSize, inRect.height())
        # Top edge
        self.sideGrips[1].setGeometry(inRect.left(), 0, inRect.width(), self.gripSize)
        # Right edge
        self.sideGrips[2].setGeometry(inRect.left() + inRect.width(), inRect.top(), self.gripSize, inRect.height())
        # Bottom edge
        self.sideGrips[3].setGeometry(self.gripSize, inRect.top() + inRect.height(), inRect.width(), self.gripSize)

    def resizeEvent(self, event):
        """Update the grips' geometry whenever the window is resized and apply rounded corners."""
        QtWidgets.QMainWindow.resizeEvent(self, event)
        self.updateGrips()
        self.round_corners()

    def round_corners(self):
        """Apply rounded corners to the window using QPainterPath."""
        radius = 9.0
        path = QPainterPath()
        path.addRoundedRect(QtCore.QRectF(self.rect()), radius, radius)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)

    def stylin( self, args ):
        with open( "style.qss", "r" ) as fh: 
            self.setStyleSheet( fh.read() )

    def clear_combined( self ):
        self.combined_list.clear()

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
            exec( code, **globals() )  # 
        except Exception as e:
            print(f"Error while executing code: {e}", file=sys.stderr)  # Capture exceptions in stderr
        finally:
            # Restore stdout and stderr after execution
            sys.stdout = old_stdout
            sys.stderr = old_stderr

    def clear_combined( self ):
        self.combined_list.clear()

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
            exec( code, globals() )  # 
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


class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initial_pos = None
        title_bar_layout = QHBoxLayout(self)
        title_bar_layout.setContentsMargins(1, 1, 1, 1)
        title_bar_layout.setSpacing(2)
        self.title = QLabel(f"{self.__class__.__name__}", self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet(
            """
        QLabel { text-transform: uppercase; font-size: 10pt; margin-left: 48px; }
        """
        )

        if title := parent.windowTitle():
            self.title.setText(title)
        title_bar_layout.addWidget(self.title)
        
        # Minimize button
        self.min_button = QToolButton(self)
        min_icon = self.create_icon_from_svg(min_svg)
        self.min_button.setIcon(QIcon(min_icon))
        self.min_button.clicked.connect(self.window().showMinimized)

        # Maximize button
        self.max_button = QToolButton(self)
        max_icon = self.create_icon_from_svg(max_svg)
        self.max_button.setIcon(QIcon(max_icon))
        self.max_button.clicked.connect(self.window().showMaximized)

        # Close button
        self.close_button = QToolButton(self)
        close_icon = self.create_icon_from_svg(close_svg)
        self.close_button.setIcon(QIcon(close_icon))
        self.close_button.clicked.connect(self.window().close)

        # Normal button (restore)
        self.normal_button = QToolButton(self)
        normal_icon = self.create_icon_from_svg(normal_svg)
        self.normal_button.setIcon(QIcon(normal_icon))
        self.normal_button.clicked.connect(self.window().showNormal)
        self.normal_button.setVisible(False)

        # Add buttons
        buttons = [self.min_button, self.normal_button, self.max_button, self.close_button]
        for button in buttons:
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            button.setFixedSize(QSize(20, 20))
            button.setStyleSheet(
                """QToolButton {
                    border: none;
                    padding: 2px;
                }
                """
            )
            title_bar_layout.addWidget(button)

    def window_state_changed(self, state):
        """Toggle the visibility of max/restore buttons based on window state."""
        if state == Qt.WindowState.WindowMaximized:
            self.normal_button.setVisible(True)
            self.max_button.setVisible(False)
        else:
            self.normal_button.setVisible(False)
            self.max_button.setVisible(True)

    def create_icon_from_svg(self, svg_data):
        svg_byte_array = QByteArray(svg_data.encode('utf-8'))
        svg_renderer = QSvgRenderer(svg_byte_array)
        pixmap = QPixmap(svg_renderer.defaultSize())
        pixmap.fill(Qt.transparent)  # Transparent background
        painter = QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()
        return pixmap

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = frameless_exec_win()
    window.show()
    sys.exit(app.exec())
