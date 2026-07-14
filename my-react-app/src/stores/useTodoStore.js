import { create } from "zustand";
import axios from "axios";

const useTodoStore = create((set, get) => ({
    // 데이터
    todo: null,
    todoList: [],

    // 액션함수
    setTodo: async (currentId) => { // 서버를 기다려야하는 동기
        const response = await axios.get('https://jsonplaceholder.typicode.com/todos/' + currentId);
        set({ todo: response.data, })
    },

    setTodoList: async () => {
        const response = await axios.get('https://jsonplaceholder.typicode.com/todos/');
        set({ todoList: response.data, })
    }
}));

export default useTodoStore;