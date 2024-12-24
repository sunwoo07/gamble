#(2^(n-1))*a원을 건다. 성공하면 (2^(n-1))*a - (2^(n-1)-1)*a = a원 이득을 보고, 
#실패하면 (2^(n-1))*a + (2^(n-1)-1)*a = ((2^n)-1)a원 손해인 상태로 다음 단계로 넘어간다.
'''
성공할 때까지 반복
2^(n-1)a원을 건다. 반복 횟수(n)를 1 로 한다. 
성공 시 : 중단한다. 총 얻은 금액을 x로 하고 x에서 y를 뺀 순수익을 출력한다. 
실패 시 : a원을 잃는다. 잃은 금액을 y에 저장한다. n을 1회 증가시킨다. 
'''
from matplotlib import pyplot as plt
import numpy as np

def martin():
    a = 1 #처음에 걸 자본금(a)
    win_probability = 0.5 #성공확률 0.5
    n = 1 #반복횟수
    loss = 0 #손해
    profit = 0 #이익
    net_profit = 0 #순이익

    while True:
        if np.random.rand() < win_probability:
            loss += (2**(n-1))*a
        else:
            profit += (2**(n-1))*a
            net_profit = profit - loss
            break
        n += 1
    
    return [n, profit, net_profit]

trial = np.arange(1,101)
result_n = []
result_profit = []
result_net_profit = []
for i in range(100):
    result_n.append(martin()[0])
    result_profit.append(martin()[1])
    result_net_profit.append(martin()[2])

fig = plt.figure(figsize=(16,9))
ax1 = fig.add_subplot(1,3,1)
ax1.plot()
ax1.set(xlim=[0., 1.], ylim=[-0.5, 2.5], title='Example', xlabel='xAxis', ylabel='yAxis')
ax2 = fig.add_subplot(1,3,2)
ax3 = fig.add_subplot(1,3,3)
plt.show()