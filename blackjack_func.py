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