from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QAction
import sys

class Editor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Griph-Pad - A lightweight editor')
        self.resize(800, 600)
        self.status = self.statusBar()
        self.status.startTimer(1000)
        self.status.showMessage('Ready')
        self.menubar = QMenuBar(self)
        self.menubar.setNativeMenuBar(True)
        self.show()

def main():
    app = QApplication(sys.argv)
    UI = Editor()
    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())