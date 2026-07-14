class Todo {
    constructor(id, title, completted, userId) {
        this.id = id;
        this.title = title;
        this.completed = completed;
        this.userId = userId;
    }
    // named parameters 방식으로 생성
    static fromJson({ id, title, completed, userId }) {
        return new Todo(id, title, completed, userId);
    }
}

export default Todo;