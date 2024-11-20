import sys
import time
from random import shuffle
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt


def create_deck():
    """6덱의 카드를 생성."""
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    return [{'suit': suit, 'value': value} for suit in suits for value in values] * 6


def calculate_score(hand):
    """카드 점수를 계산."""
    score = 0
    ace_count = 0
    for card in hand:
        if card['value'].isdigit():
            score += int(card['value'])
        elif card['value'] in ['Jack', 'Queen', 'King']:
            score += 10
        elif card['value'] == 'Ace':
            score += 11
            ace_count += 1
    while score > 21 and ace_count:
        score -= 10
        ace_count -= 1
    return score


def get_card_image(card):
    """카드 이미지를 파일 경로로 반환."""
    return f"images/{card['value']}_of_{card['suit']}.png"


class BlackjackApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.reset_game(initial=True)

    def init_ui(self):
        """UI 초기화."""
        self.setWindowTitle("Blackjack")
        self.setGeometry(200, 200, 800, 600)

        # 메인 레이아웃
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # 규칙 설명
        rules = (
            "규칙: 카드의 합이 21에 가장 가까운 사람이 승리합니다. \n"
            "King, Queen, Jack 은 10의 값을 가지며 Ace 는 1 또는 11의 값을 가집니다. \n"
            "카드의 합이 21을 초과할 시 패배하며, 딜러는 17 이상이 될 때까지 카드를 뽑습니다."
        )
        self.rules_label = QLabel(rules, self)
        self.rules_label.setFont(QFont("Arial", 12))
        self.rules_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.rules_label)

        # 상태 및 자본금 영역
        self.status_label = QLabel("게임을 시작하려면 베팅하세요", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Arial", 16))
        self.main_layout.addWidget(self.status_label)

        self.money_label = QLabel("", self)
        self.money_label.setFont(QFont("Arial", 14))
        self.money_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.money_label)

        # 베팅 영역
        self.bet_layout = QHBoxLayout()
        self.main_layout.addLayout(self.bet_layout)

        self.bet_input = QLineEdit(self)
        self.bet_input.setPlaceholderText("베팅 금액 입력")
        self.bet_layout.addWidget(self.bet_input)

        self.place_bet_button = QPushButton("베팅하기", self)
        self.place_bet_button.clicked.connect(self.place_bet)
        self.bet_layout.addWidget(self.place_bet_button)

        # 딜러와 플레이어 카드 영역
        self.dealer_label = QLabel("딜러의 카드", self)
        self.dealer_label.setFont(QFont("Arial", 14))
        self.dealer_sum_label = QLabel("딜러의 카드 합: ?", self)
        self.dealer_sum_label.setFont(QFont("Arial", 11))
        self.main_layout.addWidget(self.dealer_label)
        self.main_layout.addWidget(self.dealer_sum_label)

        self.dealer_cards_layout = QHBoxLayout()
        self.main_layout.addLayout(self.dealer_cards_layout)

        self.player_label = QLabel("플레이어의 카드", self)
        self.player_label.setFont(QFont("Arial", 14))
        self.player_sum_label = QLabel("플레이어의 카드 합: ?", self)
        self.player_sum_label.setFont(QFont("Arial", 11))
        self.main_layout.addWidget(self.player_label)
        self.main_layout.addWidget(self.player_sum_label)

        self.player_cards_layout = QHBoxLayout()
        self.main_layout.addLayout(self.player_cards_layout)

        # 버튼 영역
        self.button_layout = QHBoxLayout()
        self.main_layout.addLayout(self.button_layout)

        self.hit_button = QPushButton("카드 추가", self)
        self.hit_button.clicked.connect(self.hit)
        self.hit_button.setEnabled(False)
        self.button_layout.addWidget(self.hit_button)

        self.stand_button = QPushButton("차례 끝내기", self)
        self.stand_button.clicked.connect(self.stand)
        self.stand_button.setEnabled(False)
        self.button_layout.addWidget(self.stand_button)

        self.reset_button = QPushButton("다음 게임", self)
        self.reset_button.clicked.connect(lambda: self.reset_game(initial=False))
        self.reset_button.setEnabled(True)
        self.button_layout.addWidget(self.reset_button)

    def reset_game(self, initial=False):
        """게임 초기화."""
        if initial:
            self.player_money = 100

        self.deck = create_deck()
        shuffle(self.deck)
        self.player_hand = []
        self.dealer_hand = []
        self.bet_amount = 0

        self.update_money_display()
        self.status_label.setText("당신의 운을 시험하세요")
        self.bet_input.setEnabled(True)
        self.place_bet_button.setEnabled(True)
        self.hit_button.setEnabled(False)
        self.stand_button.setEnabled(False)

        for layout in [self.player_cards_layout, self.dealer_cards_layout]:
            for i in reversed(range(layout.count())):
                layout.itemAt(i).widget().setParent(None)

    def update_money_display(self):
        """자본금 및 베팅 금액 업데이트."""
        self.money_label.setText(f"Money: ${self.player_money} | Bet: ${self.bet_amount}")

    def place_bet(self):
        try:
            bet = int(self.bet_input.text())
            if bet <= 0 or bet > self.player_money:
                raise ValueError
            self.bet_amount = bet
            self.player_money -= bet
            self.bet_input.setEnabled(False)
            self.place_bet_button.setEnabled(False)
            self.update_money_display()
            self.start_game()
        except ValueError:
            QMessageBox.warning(self, "잘못된 금액", "올바른 금액을 입력하세요")

    def start_game(self):
        """게임 시작."""
        self.player_hand = [self.draw_card(), self.draw_card()]
        self.dealer_hand = [self.draw_card(), self.draw_card()]
        self.display_cards(hide_dealer_first_card=True)
        self.hit_button.setEnabled(True)
        self.stand_button.setEnabled(True)

        player_score = calculate_score(self.player_hand)
        if player_score == 21:
            self.status_label.setText("블랙잭! 당신이 이겼습니다.")
            self.end_game(2)

    def draw_card(self):
        """덱에서 카드 한 장 뽑기."""
        return self.deck.pop()

    def display_cards(self, hide_dealer_first_card=True):
        """카드를 화면에 표시."""
        for layout, hand, is_dealer in zip(
            [self.player_cards_layout, self.dealer_cards_layout],
            [self.player_hand, self.dealer_hand],
            [False, True],
        ):
            for i in reversed(range(layout.count())):
                layout.itemAt(i).widget().setParent(None)

            for idx, card in enumerate(hand):
                image_path = (
                    "images/Back_of_Card.png" if is_dealer and hide_dealer_first_card and idx == 0
                    else get_card_image(card)
                )
                pixmap = QPixmap(image_path).scaled(80, 120, Qt.KeepAspectRatio)
                label = QLabel(self)
                label.setPixmap(pixmap)
                layout.addWidget(label)

        self.player_sum_label.setText(f"플레이어의 카드 합: {calculate_score(self.player_hand)}")
        dealer_visible_score = calculate_score(self.dealer_hand[1:]) if hide_dealer_first_card else calculate_score(self.dealer_hand)
        self.dealer_sum_label.setText(f"딜러의 카드 합: {dealer_visible_score if hide_dealer_first_card else calculate_score(self.dealer_hand)}")

    def hit(self):
        """플레이어가 카드 받기."""
        self.player_hand.append(self.draw_card())
        self.display_cards()
        if calculate_score(self.player_hand) > 21:
            self.status_label.setText("버스트! 당신은 졌습니다.")
            self.end_game(0)

    async def stand(self):
        """플레이어가 스탠드."""
        self.display_cards(hide_dealer_first_card=False)
        while calculate_score(self.dealer_hand) < 17:
            time.sleep(1)
            self.dealer_hand.append(self.draw_card())
            self.display_cards(hide_dealer_first_card=False)

        dealer_score = calculate_score(self.dealer_hand)
        player_score = calculate_score(self.player_hand)

        if dealer_score > 21 or player_score > dealer_score:
            self.status_label.setText("당신은 이겼습니다!")
            self.end_game(1)
        elif player_score < dealer_score:
            self.status_label.setText("당신은 졌습니다.")
            self.end_game(0)
        else:
            self.status_label.setText("무승부입니다.")
            self.end_game(3)

    def end_game(self, result):
        """게임 종료 처리."""
        self.hit_button.setEnabled(False)
        self.stand_button.setEnabled(False)

        if result == 1:  # 플레이어 승리
            self.player_money += self.bet_amount * 2
        elif result == 2:  # 블랙잭
            self.player_money += self.bet_amount * 2
        elif result == 3:  # 무승부
            self.player_money += self.bet_amount

        self.update_money_display()

        if self.player_money <= 0:
            QMessageBox.information(self, "게임 종료", "자본금을 모두 잃었습니다.")
            self.reset_game(initial=True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BlackjackApp()
    window.show()
    sys.exit(app.exec_())
