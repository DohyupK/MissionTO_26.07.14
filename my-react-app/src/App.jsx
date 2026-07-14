import { Routes, Route, BrowserRouter } from "react-router-dom";
import './css/global.css';
import HomePage from "./pages/HomePage";
import CompanyPage from "./pages/CompanyPage";
import LifePage from "./pages/LifePage";
import TodoPage from "./pages/TodoPage";
import TodoListPage from "./pages/TodoListPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/company" element={<CompanyPage />} />
        <Route path="/life" element={<LifePage />} />
        <Route path="/todo" element={<TodoPage />} />
        <Route path="/todolist" element={<TodoListPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;