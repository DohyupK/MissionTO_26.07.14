import torch
import torch.nn as nn
import torch.nn.functional as F

class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        # 이미지 채널: 1 (흑백), 출력 채널: 16, 커널 크기: 3x3
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, padding=1)
        # 배치 정규화 (Batch Normalization) 레이어 추가
        self.bn1 = nn.BatchNorm2d(16)
        
        # 출력 채널: 16, 다음 출력 채널: 32, 커널 크기: 3x3
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, padding=1)
        # 배치 정규화 (Batch Normalization) 레이어 추가
        self.bn2 = nn.BatchNorm2d(32)
        
        # 맥스 풀링: 이미지 크기를 반으로 줄임 (2x2 크기)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        
        # 완전연결층 (Fully Connected Layer)
        # 예: 28x28 이미지 풀링을 2번 거치면 7x7 크기가 됨 (32개 채널 * 7 * 7)
        self.fc1 = nn.Linear(32 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10) # 최종 클래스 10개 (0~9 숫자 인식)

    def forward(self, x):
        # 입력 -> Conv1 -> BatchNorm1 -> ReLU -> Pool
        x = self.pool(F.relu(self.bn1(self.conv1(x))))
        # Conv2 -> BatchNorm2 -> ReLU -> Pool
        x = self.pool(F.relu(self.bn2(self.conv2(x))))
        
        # 1차원 벡터로 펼치기 (Flatten)
        x = x.view(-1, 32 * 7 * 7)
        
        # 완전연결층 통과
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# 모델 생성 및 구조 확인
model = SimpleCNN()
print(model)

# 테스트용 가상 데이터 주입 (배치 크기 4, 채널 1, 가로 28, 세로 28)
sample_input = torch.randn(4, 1, 28, 28)
output = model(sample_input)
print("\n출력 텐서 형태(Shape):", output.shape) # 예상 결과: torch.Size([4, 10])

# 기본적인 학습/최적화 기능 시연
print("\n--- 가상 데이터를 이용한 1단계 학습 시연 ---")
# 가상 정답 레이블 생성 (배치 크기 4, 0~9 범위의 정수)
target = torch.randint(0, 10, (4,))

# 손실 함수 및 최적화 도구 설정
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# 순전파 (Forward pass)
output = model(sample_input)
loss = criterion(output, target)
print(f"학습 전 Loss: {loss.item():.4f}")

# 역전파 및 가중치 업데이트 (Backward pass & Optimization)
optimizer.zero_grad()
loss.backward()
optimizer.step()

# 가중치 업데이트 후 결과 확인
output_after = model(sample_input)
loss_after = criterion(output_after, target)
print(f"학습 1단계 진행 후 Loss: {loss_after.item():.4f}")