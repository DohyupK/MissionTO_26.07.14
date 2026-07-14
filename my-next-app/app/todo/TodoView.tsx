'use client';
import { useEffect } from "react";
import useTodoStore from "../stores/useTodoStore";
import { useSearchParams } from "next/navigation";

export default function TodoView() {
    const { todo, setTodo } = useTodoStore();

    const searchParams = useSearchParams();
    const id = searchParams.get('id'); // "1"(문자열) 또는 null

    useEffect(() => {
        setTodo(1)
    }, [])
    return (
        <div>
            <h1>Todo</h1>
            <p>{todo?.title}</p>
            <p>id {todo?.id}</p>
            <p>completed {todo?.completed}</p>
            <p>userId {todo?.userId}</p>
        </div>
    );
}