from blackjack_func import *


class BlackjackTestApp(BlackjackApp):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_high_scores()
        self.reset_game(initial=True)

    def init_ui(self):
        super().init_ui()
        self.player_name, ok = QInputDialog.getText(self, "플레이어 닉네임", "닉네임을 입력하세요:")
        if not ok or not self.player_name.strip():
            self.player_name = "Guest"
        
        self.name_label = QLabel(f"플레이어: {self.player_name}", self)
        self.name_label.setFont(QFont("Arial", 14))
        self.main_layout.addWidget(self.name_label)

        self.high_score_label = QLabel("최고 자본금: $0", self)
        self.high_score_label.setFont(QFont("Arial", 14))
        self.main_layout.addWidget(self.high_score_label)
    
    def load_high_scores(self):
        super().load_high_scores()
        """기존 최고 점수를 로드."""
        self.high_scores = {}
        if os.path.exists("high_scores.json"):
            with open("high_scores.json", "r") as file:
                self.high_scores = json.load(file)

        self.high_score = self.high_scores.get(self.player_name, 0)
        self.high_score_label.setText(f"최고 자본금: ${self.high_score}")

    def save_high_scores(self):
        super().save_high_scores()
        """최고 점수를 저장."""
        self.high_scores[self.player_name] = max(self.high_score, self.player_money)
        with open("high_scores.json", "w") as file:
            json.dump(self.high_scores, file)

    def reset_game(self, initial=False):
        super().reset_game()
        if initial:
            self.player_money = 100
            self.high_score_label.setText(f"최고 자본금: ${self.high_score}")  

    def end_game(self, result):
        super().end_game()
        self.high_score = max(self.high_score, self.player_money)
        self.high_score_label.setText(f"최고 자본금: ${self.high_score}")
        self.save_high_scores()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BlackjackTestApp()
    window.show()
    sys.exit(app.exec_())
