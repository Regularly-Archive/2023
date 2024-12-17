import App from './App';
import TodoApp from './TodoApp';
import Markdown from './Markodwn';
import { createBrowserRouter } from "react-router-dom";

const router = createBrowserRouter([
    {
      name: 'Home',
      path: "/",
      element: <App />
    },
    {
      name: 'Todo',
      path: "todo",
      element: <TodoApp />,
    },
    {
      name: 'React',
      path: 'https://react.dev/',
      external: true
    },
    {
      name: 'Markdown',
      path: "markdown",
      element: <Markdown />,
    }
  ]);

export default router;

