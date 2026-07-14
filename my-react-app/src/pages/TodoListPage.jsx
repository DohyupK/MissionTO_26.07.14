import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import useTodoStore from "../stores/useTodoStore";

export default function TodoListPage() {
    const { todoList, setTodoList } = useTodoStore();
    const [loading, setLoading] = useState(true);

    const getTodos = async () => {
        await setTodoList()
        setLoading(false);
    };

    useEffect(() => {
        getTodos();
    }, []);

    return (
        <div className="todo-page">
            <div className="todo-page__inner">
                <header className="todo-header">
                    <span className="todo-header__tag">TODO</span>
                    <h1 className="todo-header__title">할 일 목록</h1>
                    <p className="todo-header__id">
                        총 {loading ? "-" : todoList.length}개
                    </p>
                </header>

                {loading ? (
                    <div className="todo-loading">불러오는 중...</div>
                ) : (
                    <ul className="todo-items">
                        {todoList.map((todo) => (
                            <li key={todo.id} className="todo-items__card">
                                <div className="todo-items__top">
                                    <span
                                        className={`todo-badge ${todo.completed ? "todo-badge--done" : "todo-badge--pending"}`}
                                    >
                                        {todo.completed ? "완료" : "미완료"}
                                    </span>
                                    <span className="todo-items__id">#{todo.id}</span>
                                </div>
                                <p className="todo-items__title">{todo.title}</p>
                                <Link
                                    to={`/todo?id=${todo.id}`}
                                    className="todo-items__link"
                                >
                                    상세 보기 →
                                </Link>
                            </li>
                        ))}
                    </ul>
                )}
            </div>
        </div>
    );
}
