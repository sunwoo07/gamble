from blackjack.blackjack import *


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BlackjackApp()
    window.show()
    sys.exit(app.exec_())