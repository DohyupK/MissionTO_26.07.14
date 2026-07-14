import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정 (Windows: Malgun Gothic)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('data.csv')

df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)
monthly_data = df.resample('ME').sum()  # 월별 합계 계산


plt.figure(figsize=(10, 6))
plt.plot(monthly_data.index, monthly_data['value'], marker='o')
plt.title('월별 데이터 변화')
plt.xlabel('Date')
plt.ylabel('Value')
plt.grid(True)

# 그래프를 이미지 파일로 저장
plt.savefig('monthly_chart.png', dpi=300, bbox_inches='tight')

plt.show()
