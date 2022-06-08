from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import webbrowser
import sys

ICON = "assets/icon.png"


class Editor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Griph-Pad - A lightweight editor")
        self.setWindowIcon(QIcon(ICON))
        self.resize(800, 600)
        self.status = self.statusBar()
        self.status.startTimer(1000)
        self.status.showMessage("Ready")
        self.menubar = self.menuBar()

        # Menu bars
        # File | Edit | View | Help | About
        # ============================================================
        # File -> New, Open, Save, Save As, Close, Exit
        # Edit -> Undo, Redo, Cut, Copy, Paste, Delete, Select All
        # View -> Font, Font Size, Line Wrap, Status Bar, Line Numbers, Full Screen
        # Help -> Report Bug
        # About -> About Griph-Pad, About Qt, License, Credits
        self.initMenuBar()
        self.show()

    def initMenuBar(self):
        self.file_menu = self.menubar.addMenu("File")
        self.edit_menu = self.menubar.addMenu("Edit")
        self.view_menu = self.menubar.addMenu("View")
        self.help_menu = self.menubar.addMenu("Help")
        self.about_menu = self.menubar.addMenu("About")

        self.new_action = QAction("New", self)
        self.new_action.setShortcut("Ctrl+N")
        self.new_action.setStatusTip("Create a new file")
        self.new_action.triggered.connect(self.new)

        self.open_action = QAction("Open", self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.setStatusTip("Open a file")
        self.open_action.triggered.connect(self.open)

        self.save_action = QAction("Save", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.setStatusTip("Save the document")
        self.save_action.triggered.connect(self.save)

        self.save_as_action = QAction("Save As", self)
        self.save_as_action.setStatusTip(
            "Save the document without overwriting the current file"
        )
        self.save_as_action.setShortcut("Ctrl+Shift+S")
        self.save_as_action.triggered.connect(self.save)

        self.exit_action = QAction("Exit", self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.setStatusTip("Exit Griph-Pad")

        self.file_menu.addAction(self.new_action)
        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.save_as_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_action)

        self.undo_action = QAction("Undo", self)
        self.undo_action.setShortcut("Ctrl+Z")
        self.undo_action.setStatusTip("Undo")
        self.undo_action.triggered.connect(self.undo)

        self.redo_action = QAction("Redo", self)
        self.redo_action.setShortcut("Ctrl+Y")
        self.redo_action.setStatusTip("Redo")
        self.redo_action.triggered.connect(self.redo)

        self.cut_action = QAction("Cut", self)
        self.cut_action.setShortcut("Ctrl+X")
        self.cut_action.setStatusTip("Cut the selection")
        self.cut_action.triggered.connect(self.cut)

        self.copy_action = QAction("Copy", self)
        self.copy_action.setShortcut("Ctrl+C")
        self.copy_action.setStatusTip("Copy the selection")
        self.copy_action.triggered.connect(self.copy)

        self.paste_action = QAction("Paste", self)
        self.paste_action.setShortcut("Ctrl+V")
        self.paste_action.setStatusTip("Paste from system clipboard")
        self.paste_action.triggered.connect(self.paste)

        self.delete_action = QAction("Delete", self)
        self.delete_action.setShortcut("Del")
        self.delete_action.setStatusTip(
            "Delete the selection or the character after the cursor"
        )
        self.delete_action.triggered.connect(self.delete)

        self.select_all_action = QAction("Select All", self)
        self.select_all_action.setShortcut("Ctrl+A")
        self.select_all_action.setStatusTip("Select all the text")
        self.select_all_action.triggered.connect(self.select_all)

        self.edit_menu.addAction(self.undo_action)
        self.edit_menu.addAction(self.redo_action)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.cut_action)
        self.edit_menu.addAction(self.copy_action)
        self.edit_menu.addAction(self.paste_action)
        self.edit_menu.addAction(self.delete_action)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.select_all_action)

        self.font_action = QAction("Font", self)
        self.font_action.setStatusTip("Change the current font")
        self.font_action.setShortcut("Ctrl+shift+F")
        self.font_action.triggered.connect(self.font)

        self.font_size_action = QAction("Font Size", self)
        self.font_size_action.setStatusTip("Change the current font size")
        self.font_size_action.setShortcut("Ctrl+shift+S")
        self.font_size_action.triggered.connect(self.font_size)

        self.line_wrap_action = QAction("Line Wrap", self)
        self.line_wrap_action.setStatusTip("Toggle line wrap")
        self.line_wrap_action.setShortcut("Ctrl+shift+W")
        self.line_wrap_action.triggered.connect(self.line_wrap)
        self.line_wrap_action.setCheckable(True)

        self.status_bar_action = QAction("Status Bar", self)
        self.status_bar_action.setStatusTip("Toggle status bar")
        self.status_bar_action.setShortcut("Ctrl+shift+B")
        self.status_bar_action.triggered.connect(self.status_bar)
        self.status_bar_action.setCheckable(True)

        self.line_number_action = QAction("Line Numbers", self)
        self.line_number_action.setStatusTip("Toggle line numbers")
        self.line_number_action.setShortcut("Ctrl+shift+L")
        self.line_number_action.triggered.connect(self.line_number)
        self.line_number_action.setCheckable(True)

        self.enter_full_screen_action = QAction("Full Screen", self)
        self.enter_full_screen_action.setStatusTip("Enter/Exit full screen mode")
        self.enter_full_screen_action.setShortcut("F11")
        self.enter_full_screen_action.triggered.connect(self.enter_full_screen)
        self.enter_full_screen_action.setCheckable(True)

        self.view_menu.addAction(self.font_action)
        self.view_menu.addAction(self.font_size_action)
        self.view_menu.addAction(self.line_wrap_action)
        self.view_menu.addAction(self.status_bar_action)
        self.view_menu.addSeparator()
        self.view_menu.addAction(self.line_number_action)
        self.view_menu.addAction(self.enter_full_screen_action)

        self.report_bug_action = QAction("Report Bug", self)
        self.report_bug_action.setStatusTip("Report a bug (Via Github)")
        self.report_bug_action.setShortcut("Ctrl+B")
        self.report_bug_action.triggered.connect(self.report_bug)

        self.help_menu.addAction(self.report_bug_action)

        self.about_action = QAction("About", self)
        self.about_action.setStatusTip("About Griph-Pad")
        self.about_action.setShortcut("Ctrl+Shift+A")
        self.about_action.triggered.connect(self.about)

        self.about_qt_action = QAction("About Qt", self)
        self.about_qt_action.setStatusTip("About Qt Framework (PyQt5)")
        self.about_qt_action.setShortcut("Ctrl+Shift+Q")
        self.about_qt_action.triggered.connect(self.about_qt)

        self.license = QAction("License", self)
        self.license.setStatusTip("License Information")
        self.license.setShortcut("Ctrl+Alt+L")
        self.license.triggered.connect(self.license_)

        self.credits = QAction("Credits", self)
        self.credits.setStatusTip("Credits and Thanks")
        self.credits.setShortcut("Ctrl+Shift+C")
        self.credits.triggered.connect(self.credits_)

        self.about_menu.addAction(self.about_action)
        self.about_menu.addAction(self.about_qt_action)
        self.about_menu.addAction(self.license)
        self.about_menu.addAction(self.credits)

    def new(self):
        print("New file")

    def open(self):
        print("Open file")

    def save(self):
        print("Save file")

    def exit(self):
        print("Exit")

    def copy(self):
        print("Copy")

    def paste(self):
        print("Paste")

    def cut(self):
        print("Cut")

    def undo(self):
        print("Undo")

    def redo(self):
        print("Redo")

    def delete(self):
        print("Delete")

    def select_all(self):
        print("Select all")

    def status_bar(self):
        self.status.hide() if self.status.isVisible() else self.status.show()

    def font(self):
        print("Font")

    def font_size(self):
        print("Font size")

    def line_wrap(self):
        print("Line wrap")

    def report_bug(self):
        webbrowser.open_new_tab(
            "https://github.com/Griphitor/Griph-pad/issues/new/choose"
        )

    def about(self):
        print("About")

    def about_qt(self):
        QMessageBox.aboutQt(self, "About Qt")

    def license_(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("License Information")
        msg.setText('The license is for the "Griph-Pad" application. Not Qt.')
        msg.setInformativeText(
            
            "MIT License\n"
            "\n"
            "Copyright (c) 2022-Present Griphitor Team <https://github.com/Griphitor>\n"
            "\n"
            "Permission is hereby granted, free of charge, to any person obtaining a copy\n"
            "of this software and associated documentation files (the 'Software'), to deal\n"
            "in the Software without restriction, including without limitation the rights\n"
            "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
            "copies of the Software, and to permit persons to whom the Software is\n"
            "furnished to do so, subject to the following conditions:\n"
            "\n"
            "The above copyright notice and this permission notice shall be included in all\n"
            "copies or substantial portions of the Software.\n"
            "\n"
            "THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
            "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
            "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
            "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
            "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
            "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n"
            "SOFTWARE."
        )
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setWindowIcon(self.windowIcon())
        msg.exec_()
        

    def credits_(self):
        print("Credits")

    def line_number(self):
        print("Line number")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Line numbers are not implemented (yet)")
        msg.setInformativeText("Sorry about that, I'm working on it")
        msg.setWindowTitle("Not implemented Error")
        msg.setWindowIcon(self.windowIcon())
        msg.exec_()
        del msg
        self.line_number_action.setChecked(False)

    def closeEvent(self, event):
        event.accept()

    def enter_full_screen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()


def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    UI = Editor()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
