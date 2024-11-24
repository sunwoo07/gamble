import matplotlib.pyplot as plt
import numpy as np

# 초기 조건 및 매개 변수 설정
initial_money = 100000  # 시작 자본금
win_rate = 0.49         # 승률 49%
n_trials = 50           # 시행 횟수

# 결과를 저장할 변수 초기화
trials = np.arange(1, n_trials + 1)  # 시행 횟수 1부터 n_trials까지
wins = np.zeros(n_trials)            # 누적 승리 횟수를 저장할 배열
money = np.zeros(n_trials)           # 자본금을 저장할 배열

# 시뮬레이션
current_money = initial_money
current_wins = 0

for i in range(n_trials):
    # 승률에 따라 승리 또는 패배 결정
    bat = current_money * (np.random.randint(1, 101)/100)  # 배팅 금액은 자본의 0~100%에서 랜덤 설정
    current_money = current_money - bat  # 자본에서 배팅 금액 차감
    if np.random.rand() < win_rate:
        current_money = current_money + (bat * 2)  # 승리 시 자본이 배팅 금액의 2배 상승
        current_wins += 1
    # 패배 시 배팅 금액 증발 -> 현재 코드에서 'else'는 사실 불필요함, 패배 시에는 그냥 넘어간다.
    
    # 누적 승리 횟수와 자본금을 배열에 기록
    wins[i] = current_wins
    money[i] = current_money

# 그래프 그리기
fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle('Blackjack Simulation')

# 누적 승리 횟수 그래프
ax1.plot(trials, wins, color="blue", label="win")
ax1.set_xlabel('Trials (n)')
ax1.set_ylabel('Win Count')
ax1.legend()
ax1.grid(True)

# 자본금 변화 그래프
ax2.plot(trials, money, color="green", label="Money")
ax2.set_xlabel('Trials (n)')
ax2.set_ylabel('Money ($)')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()
