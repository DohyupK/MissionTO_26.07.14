import axios from "axios";
import { useEffect, useState } from "react"
import useTodoStore from "../stores/useTodoStore";

export default function TodoPage() {
    const { todo, setTodo } = useTodoStore();
    const [loading, setLoading] = useState(true);

    // window.location.search는 URL에서 "?id=1" 부분만 가져옵니다.
    const searchParams = new URLSearchParams(window.location.search);
    // 'id' 키의 값을 추출하여 상태에 저장합니다.
    const currentId = searchParams.get('id');

    const getTodo = async () => {
        await setTodo(currentId)
        setLoading(false);
    }

    useEffect(() => {
        getTodo();
    }, []);

    return (
        <div>
            <h1>TodoPage</h1>
            <p>Title: {todo?.title}</p>
            <p>Completed: {todo?.completed ? '완료' : '미완료'}</p>
            <p>ID: {todo?.id}</p>
            <p>userId: {todo?.userId}</p>
        </div>
    )
}