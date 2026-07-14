import matplotlib.pyplot as plt

x = [1, 2, 3, 4]
y1 = [1, 4, 9, 16]
y2 = [1, 2, 3, 4]

# 2개의 행과 1개의 열을 가진 subplot을 생성
fig, axs = plt.subplots(2)

axs[0].plot(x, y1)
axs[0].set_title('Quadratic')

axs[1].plot(x, y2)
axs[1].set_title('Linear')

plt.tight_layout()  # 자동으로 서브플롯 간의 간격을 조정
plt.show()