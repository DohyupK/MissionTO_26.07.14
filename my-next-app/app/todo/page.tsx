import { Suspense } from "react";
import TodoView from "./TodoView";

export default function Todo() {
    return (
        <Suspense fallback={<div>Loading...</div>}>
            <TodoView />
        </Suspense>
    );
}