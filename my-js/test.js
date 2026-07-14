// 동적타입 var, let, const
// var 재선언, 재할당 다 가능
var a = 1;
var a = 2;
a = 3;
a = 4.12
a = true;  //false

// let 재선언 불가, 재할당 가능
let b = 1;
// let b = 2;
b = 2;

// const 재선언 불가, 재할당 불가, 초기화 필수
const serverAddress = '127.0.0.1';

// 여러개 받는 타입 : 배열, 오브젝트
// 배열
let arr = ['apple', 'banana', 'cherry'];
console.log(arr[0]);

// 오브젝트
let user = {
    name: 'John',
    age: 20,
    email: 'john@example.com'
}
var userName = user['name'];
var userName = user.name;

// 함수
function add(num1, num2) {
    var sum = num1 + num2;
    return sum;
}
var result = add(10, 20);
console.log(result);

var score = 100;
if (score >= 90) {
    console.log('A');
} else if (score >= 80) {
    console.log('B');
} else if (score >= 70) {
    console.log('C');
} else {
    console.log('F');
}

for (var i = 0; i < 10; i++) {
    console.log(i);
}

var users = ['John', 'Jane', 'Jim', 'Jill'];
for (var u of users) {
    console.log(u);
}

class Animal {
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }
    eat() {
        console.log(this.name + ' is eating');
    }
    sleep() {
        console.log(this.name + ' is sleeping');
    }
}
var dog = new Animal('dog', 10);
dog.eat();