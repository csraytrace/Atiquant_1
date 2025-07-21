import sys
import PyQt5
from PyMca5.PyMcaGui.pymca import PyMcaMain

def main():
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    window = PyMcaMain.PyMcaMain()
    window.show()
    sys.exit(app.exec_())
#if __name__ == "__main__":
 #   main()
main()
