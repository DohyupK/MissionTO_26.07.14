class Todo {
    id: number;
    title: string;
    completed: boolean;
    userId: number;

    // named constructor
    constructor({ id, title, completed, userId }: { id: number, title: string, completed: boolean, userId: number }) {
        this.id = id;
        this.title = title;
        this.completed = completed;
        this.userId = userId;
    }

    // fromJson
    static fromJson(json: any): Todo {
        return new Todo({
            id: json.id,
            title: json.title,
            completed: json.completed,
            userId: json.userId,
        });
    }

    // fromJsonArray
    static fromJsonArray(json: any[]): Todo[] {
        return json.map(Todo.fromJson);
    }
}