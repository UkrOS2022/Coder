from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
import subprocess
import sys
import webbrowser

class Coder(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Coder')
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(50, 50, 400, 300)

        self.tabWidget = QTabWidget()
        self.setCentralWidget(self.tabWidget)

        # Create the initial tab
        self.newFile()

        # File Actions
        newAction = QAction('New', self)
        newAction.triggered.connect(self.newFile)

        openAction = QAction('Open', self)
        openAction.triggered.connect(self.openFile)

        saveAction = QAction('Save', self)
        saveAction.triggered.connect(self.saveFile)

        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(self.close)

        # Edit Actions
        copyAction = QAction('Copy', self)
        copyAction.triggered.connect(self.copy)

        cutAction = QAction('Cut', self)
        cutAction.triggered.connect(self.cut)

        pasteAction = QAction('Paste', self)
        pasteAction.triggered.connect(self.paste)

        findAction = QAction('Find', self)
        findAction.triggered.connect(self.findText)

        # Debug Actions
        pythonAction = QAction('Python', self)
        pythonAction.triggered.connect(self.debugPython)

        htmlAction = QAction('HTML', self)
        htmlAction.triggered.connect(self.debugHTML)

        # Help Actions
        aboutAction = QAction('About', self)
        aboutAction.triggered.connect(self.about)

        menubar = self.menuBar()

        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)

        editMenu = menubar.addMenu('Edit')
        editMenu.addAction(copyAction)
        editMenu.addAction(cutAction)
        editMenu.addAction(pasteAction)
        editMenu.addAction(findAction)

        debugMenu = menubar.addMenu('Debug')
        debugMenu.addAction(pythonAction)
        debugMenu.addAction(htmlAction)

        helpMenu = menubar.addMenu('Help')
        helpMenu.addAction(aboutAction)
        
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        # Add labels to display line and column information
        self.lineLabel = QLabel(' Line: 1 ')
        self.columnLabel = QLabel(' Column: 1 ')

        self.statusBar.addPermanentWidget(self.lineLabel)
        self.statusBar.addPermanentWidget(self.columnLabel)
        
        self.show()

    def updateStatusBar(self):
        current_text_edit = self.currentTextEdit()

        if current_text_edit:
            cursor = current_text_edit.textCursor()
            line = cursor.blockNumber() + 1  # Line numbers start from 1
            column = cursor.columnNumber() + 1  # Column numbers start from 1

            self.lineLabel.setText(f' Line: {line} ')
            self.columnLabel.setText(f' Column: {column} ')

    def newFile(self):
        textEdit = QTextEdit()
        textEdit.cursorPositionChanged.connect(self.updateStatusBar)  # Connect cursor position change signal
        index = self.tabWidget.addTab(textEdit, f'Tab {self.tabWidget.count() + 1}')

        # Make the tab closable with a custom close button
        close_button = QPushButton("x")
        close_button.clicked.connect(lambda _, i=index: self.closeTab(i))

        # Set the width and height to make it square
        close_button.setFixedSize(20, 20)

        tab_bar = self.tabWidget.tabBar()
        tab_bar.setTabButton(index, QTabBar.RightSide, close_button)

    def closeTab(self, index):
        self.tabWidget.removeTab(index)

    def copy(self):
        self.currentTextEdit().copy()

    def cut(self):
        self.currentTextEdit().cut()

    def paste(self):
        self.currentTextEdit().paste()

    def currentTextEdit(self):
        return self.tabWidget.currentWidget().findChild(QTextEdit)

    def openFile(self, file_path=None):
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
            text_edit = QTextEdit()
            text_edit.setPlainText(content)

            # Enable horizontal scrollbar
            text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

            # Extract the file name from the path
            file_title = QFileInfo(file_path).fileName()

            index = self.tabWidget.addTab(text_edit, f'{file_title}')

            # Make the tab closable with a custom close button
            close_button = QPushButton("x")
            close_button.clicked.connect(lambda _, i=index: self.closeTab(i))

            # Set the width and height to make it square
            close_button.setFixedSize(20, 20)

            tab_bar = self.tabWidget.tabBar()
            tab_bar.setTabButton(index, QTabBar.RightSide, close_button)
    
    def currentTextEdit(self):
        current_widget = self.tabWidget.currentWidget()
        if current_widget and isinstance(current_widget, QTextEdit):
            return current_widget
        return None
            
    def saveFile(self):
        current_widget = self.currentTextEdit()
        if current_widget:
            file_name, _ = QFileDialog.getSaveFileName(None, "Save File", "", "Text Files (*.txt);;All Files (*)")
            if file_name:
                with open(file_name, 'w') as file:
                    file.write(current_widget.toPlainText())

    def findText(self):
        find_dialog = FindDialog(self)
        find_dialog.show()

    def debugPython(self):
        current_text_edit = self.currentTextEdit()
        if current_text_edit:
            code = current_text_edit.toPlainText()
            file_path = os.path.expanduser(f'~/.programdates/temp.py')
            with open(file_path, "w") as f:
                f.write(code)
            if sys.platform == 'win32':
                subprocess.run(["start", "cmd", "/k", "python", file_path], shell=True)
            elif sys.platform == 'darwin':
                subprocess.run(["open", "-a", "Terminal", file_path])
            elif sys.platform == 'linux':
                subprocess.run(["x-terminal-emulator", "-e", "python3", file_path])

    def debugHTML(self):
        current_text_edit = self.currentTextEdit()
        if current_text_edit:
            code = current_text_edit.toPlainText()
            file_path = os.path.expanduser(f'~/.programdates/temp.html')
            with open(file_path, "w") as f:
                f.write(code)
            webbrowser.open_new_tab(file_path)
    
    def about(self):
        about_content = "Coder\nVersion: 1.0.0 beta\nAuthor: UkrOS"

        about_tab = QTextEdit()
        about_tab.setPlainText(about_content)
        about_tab.setReadOnly(True)

        index = self.tabWidget.addTab(about_tab, "About")

        # Make the tab closable with a custom close button
        close_button = QPushButton("x")
        close_button.clicked.connect(lambda _, i=index: self.closeTab(i))

        # Set the width and height to make it square
        close_button.setFixedSize(20, 20)

        tab_bar = self.tabWidget.tabBar()
        tab_bar.setTabButton(index, QTabBar.RightSide, close_button)
    

class FindDialog(QDialog):
    def __init__(self, parent=None):
        super(FindDialog, self).__init__(parent)
        self.setWindowTitle('Find Text')

        layout = QVBoxLayout()

        self.find_input = QLineEdit(self)
        self.find_input.setPlaceholderText('Enter text to find')
        layout.addWidget(self.find_input)

        find_button = QPushButton('Find', self)
        find_button.clicked.connect(self.find)
        layout.addWidget(find_button)

        self.setLayout(layout)

    def find(self):
        text_to_find = self.find_input.text()

        if text_to_find:
            current_text_edit = self.parent().currentTextEdit()

            if current_text_edit:
                cursor = QTextCursor(current_text_edit.document())
                format = QTextCharFormat()

                while not cursor.isNull() and not cursor.atEnd():
                    cursor = cursor.document().find(QRegularExpression(text_to_find), cursor)
                    if not cursor.isNull():
                        cursor.setPosition(cursor.position(), QTextCursor.KeepAnchor)
                        current_text_edit.setTextCursor(cursor)
                        break


if __name__ == '__main__':
    app = QApplication(sys.argv)
    code = Coder()

    # Check if a file path argument is provided
    if len(sys.argv) > 1:
        file_path = sys.argv[1]

        # Open the file and display its content in a new tab
        code.openFile(file_path)

    sys.exit(app.exec_())
