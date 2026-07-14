#1. elif, else 는 선택사항
#2. if, elif, else 는 세트!
#3. 조건식 아무거나
#4. 첫번째로 true이면 로직 실행 후 세트 탈출!


import dataclasses
from re import match
score = input('점수를 입력하세요:')
score = int(score)


if score==100 :
    print('만점 입니다.')

elif score==90:
    print('90점 이상입니다.')

elif score == 80:
    print('80점 이상입니다.')

else:
    print('아쉽습니다.')

match score:
    case s if s == 100:
        print('만점 입니다.')
    case s if s >= 90:
        print('90점 이상입니다.')
    case s if s >= 80:
        print('80점 이상입니다.')
    case _:
        print('아쉽습니다.')


