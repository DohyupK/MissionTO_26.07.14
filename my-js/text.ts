// 타입 명확성 (숫자: number, 문자: string)
var a: number = 1;

function plus(a: number, b: number): number {
    return a + b;
}

// 인터페이스
interface Item {
    name: string;
    price: number;
    quentity: number;
    maker: string;
}

var item1: Item = {
    name: "apple",
    price: 1000,
    quentity: 10,
    maker: '나의농장'
}

var item2: Item = {
    name: "banana",
    price: 2000,
    quentity: 20,
    maker: '우리농장'
}