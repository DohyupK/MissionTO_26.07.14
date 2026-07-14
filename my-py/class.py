

class Animal:
    #생성자 : 클래스를 사용할때 호출되는 함수!.
    def __init__(self, type, name, age):
        self.type = type
        self.name = name
        self.age = age

    
    def introduce(self):
        print(f'{self.type} 의 이름은 {self.name}이고, 나이는 {self.age}살입니다.')
    

    def eat_food(self,food):
        print(f'{self.name} 이 {food} 를 먹고 있습니다.')


dog = Animal('강아지','멍멍이',2)
cat = Animal('고양이','야옹이',4)

dog.introduce()
cat.introduce()

dog.eat_food('고기')
cat.eat_food('참치')
