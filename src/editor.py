import math
import sys
import textwrap
import time
import os
from pathlib import Path
from collections import defaultdict

from PyQt5.Qsci import QsciLexerCustom, QsciScintilla
from PyQt5.Qt import (
    QFont,
    QColor,
    QShortcut,
)

from pygments import lexers, styles, highlight, formatters
from pygments.lexer import Error, RegexLexer, Text, _TokenType
from pygments.style import Style
from PyQt5.QtWidgets import QApplication
import json

tf = os.path.join(os.getcwd(), "themes")
THEMES = {}
for file in os.listdir(tf):
    THEMES.update({file.replace(".json", ""): json.load(open(os.path.join(tf, file)))})


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"


class ViewLexer(QsciLexerCustom):
    def __init__(self, lexer_name, style_name, font: QFont):
        super().__init__()

        # Lexer + Style
        self.pyg_style = styles.get_style_by_name(style_name)
        self.pyg_lexer = lexers.get_lexer_by_name(lexer_name, stripnl=False)
        self.cache = {0: ("root",)}
        self.extra_style = THEMES[style_name]

        # Generate QScintilla styles
        self.font = font
        self.token_styles = {}
        index = 0
        for k, v in self.pyg_style:
            self.token_styles[k] = index
            if v.get("color", None):
                self.setColor(QColor(f"#{v['color']}"), index)
            if v.get("bgcolor", None):
                self.setPaper(QColor(f"#{v['bgcolor']}"), index)

            self.setFont(self.font, index)
            index += 1

    def defaultPaper(self, style):
        return QColor(self.extra_style["background"])

    def language(self):
        return self.pyg_lexer.name

    def get_tokens_unprocessed(self, text, stack=("root",)):
        """
        Split ``text`` into (tokentype, text) pairs.

        ``stack`` is the inital stack (default: ``['root']``)
        """
        lexer = self.pyg_lexer
        pos = 0
        tokendefs = lexer._tokens
        statestack = list(stack)
        statetokens = tokendefs[statestack[-1]]
        while 1:
            for rexmatch, action, new_state in statetokens:
                m = rexmatch(text, pos)
                if m:
                    if action is not None:
                        if type(action) is _TokenType:
                            yield pos, action, m.group()
                        else:
                            for item in action(lexer, m):
                                yield item
                    pos = m.end()
                    if new_state is not None:
                        # state transition
                        if isinstance(new_state, tuple):
                            for state in new_state:
                                if state == "#pop":
                                    statestack.pop()
                                elif state == "#push":
                                    statestack.append(statestack[-1])
                                else:
                                    statestack.append(state)
                        elif isinstance(new_state, int):
                            # pop
                            del statestack[new_state:]
                        elif new_state == "#push":
                            statestack.append(statestack[-1])
                        else:
                            assert False, "wrong state def: %r" % new_state
                        statetokens = tokendefs[statestack[-1]]
                    break
            else:
                # We are here only if all state tokens have been considered
                # and there was not a match on any of them.
                try:
                    if text[pos] == "\n":
                        # at EOL, reset state to "root"
                        statestack = ["root"]
                        statetokens = tokendefs["root"]
                        yield pos, Text, "\n"
                        pos += 1
                        continue
                    yield pos, Error, text[pos]
                    pos += 1
                except IndexError:
                    break

    def highlight_slow(self, start, end):
        style = self.pyg_style
        view = self.editor()
        code = view.text()[start:]
        tokensource = self.get_tokens_unprocessed(code)

        self.startStyling(start)
        for _, ttype, value in tokensource:
            self.setStyling(len(value), self.token_styles[ttype])

    def styleText(self, start, end):
        view = self.editor()
        t_start = time.time()
        self.highlight_slow(start, end)
        t_elapsed = time.time() - t_start
        len_text = len(view.text())
        text_size = convert_size(len_text)
        view.setWindowTitle(
            f"Text size: {len_text} - {text_size} Elapsed: {t_elapsed}s"
        )

    def description(self, style_nr):
        return str(style_nr)


class View(QsciScintilla):
    def __init__(self, lexer_name, style_name):
        super().__init__()
        view = self
        # -------- Shortcuts --------
        self.font_size = 8
        self.font = QFont("JetBrains Mono", self.font_size)
        self.setFont(self.font)
        self.setTabWidth(4)
        self.setText("Hello")

        # -------- Lexer --------
        self.setEolMode(QsciScintilla.EolUnix)
        self.lexer = ViewLexer(lexer_name, style_name, self.font)
        self.setLexer(self.lexer)

        # # -------- Multiselection --------
        self.SendScintilla(view.SCI_SETMULTIPLESELECTION, True)
        self.SendScintilla(view.SCI_SETMULTIPASTE, 1)
        self.SendScintilla(view.SCI_SETADDITIONALSELECTIONTYPING, True)

        # -------- Extra settings --------
        self.set_extra_settings(THEMES[style_name])

    def get_line_separator(self):
        m = self.eolMode()
        if m == QsciScintilla.EolWindows:
            eol = "\r\n"
        elif m == QsciScintilla.EolUnix:
            eol = "\n"
        elif m == QsciScintilla.EolMac:
            eol = "\r"
        else:
            eol = ""
        return eol

    def set_extra_settings(self, dct):
        self.setIndentationGuidesBackgroundColor(QColor(0, 0, 255, 0))
        self.setIndentationGuidesForegroundColor(QColor(0, 255, 0, 0))

        if "caret" in dct:
            self.setCaretForegroundColor(QColor(dct["caret"]))

        if "line_highlight" in dct:
            self.setCaretLineBackgroundColor(QColor(dct["line_highlight"]))

        if "brackets_background" in dct:
            self.setMatchedBraceBackgroundColor(QColor(dct["brackets_background"]))

        if "brackets_foreground" in dct:
            self.setMatchedBraceForegroundColor(QColor(dct["brackets_foreground"]))

        if "selection" in dct:
            self.setSelectionBackgroundColor(QColor(dct["selection"]))

        if "background" in dct:
            c = QColor(dct["background"])
            self.resetFoldMarginColors()
            self.setFoldMarginColors(c, c)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = View("python", "monokai")
    # view.setText(textwrap.dedent("""\
    #     '''
    #     Ctrl+1 = You'll decrease the size of existing text
    #     Ctrl+2 = You'll increase the size of existing text

    #     Warning: Check the window title to see how long it takes rehighlighting
    #     '''
    # """))
    view.resize(800, 600)
    view.show()
    app.exec_()
