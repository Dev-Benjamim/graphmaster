#!/usr/bin/env python
from PySide6.QtWidgets import QApplication
from window import Window
import sys


def main() -> None:
    app: QApplication = QApplication(sys.argv)

    window: Window = Window()
    window.show()

    app.exec()

if __name__ == "__main__":
    main()
