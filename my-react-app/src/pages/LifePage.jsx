import { useEffect, useState } from "react";

export default function LifePage() {

    const [text, setText] = useState('Hello World');

    useEffect(() => {
        alert('LifePage');
    }, []);

    useEffect(() => {
        alert('text가 변경되었습니다.');
    }, [text]);

    const handleClick = () => {
        setText('안녕하세요');
    }

    return (
        <div>
            <h1>LifePage : {text}</h1>
            <button onClick={handleClick}>버튼</button>
        </div>
    )
}