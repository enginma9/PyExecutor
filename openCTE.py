from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTabBar, QFileDialog
from PyQt5 import QtGui
from CustomText import CustomTextEdit
from pathlib import Path
import sys, os, copy


class text_window( CustomTextEdit ):
    def __init__( self, *args, **kwargs ):
        if not QApplication.instance():
            self.app = QApplication( sys.argv )
        super().__init__( *args, **kwargs )

        styleFile = "style.qss" 
        try:
            with open(styleFile, "r") as fh: 
                self.setStyleSheet(fh.read())
        except:
            pass
        self.title = 'openCTE.py '
        self.setWindowTitle( self.title )
        self.setGeometry(100, 100, 1250, 230)
        self.open_file_dialog()
        self.show()
    
    def set_files( self, filepath ):
        with open( filepath ) as this_file:
            self.setText( this_file.read() )

    def open_file_dialog( self ):
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select a File", 
            str( os.path.join( Path.home(), "/home/jojo/Desktop/Junkdrawer/Python" ) ),
            "Text (*.txt *.cpp *.hpp *.h *.py *.md *.js *.qss *.css *.desktop)"
        )
        if filename:
            path = Path( filename )
            self.set_files( str( path ) )
            print(path)
            #self.filename_edit.setText(str(path))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    CT = text_window()
    sys.exit(app.exec())
    

