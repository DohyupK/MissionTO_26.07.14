import axios from "axios";
import { create } from "zustand";

interface TodoStoreState {
    todo: Todo | null
    todos: Todo[]
    setTodo: (id: number) => Promise<void>
    test: (name: string) => number
}

const useTodoStore = create<TodoStoreState>((set, get) => ({
    //데이터
    todo: null,
    todos: [],

    //액션함수
    setTodo: async (id: number) => {
        var response = await axios.get('https://jsonplaceholder.typicode.com/todos/' + id)
        set({ todo: Todo.fromJson(response.data) })
    },
    setTodos: async () => {
        var response = await axios.get('https://jsonplaceholder.typicode.com/todos')
        set({ todos: Todo.fromJsonArray(response.data) })
    },

    test: (name: string): number => {
        return 10
    }
}));

export default useTodoStore;