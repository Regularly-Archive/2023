import logo from './logo.svg';
import './App.css';
import router from './router';
import { Link } from "react-router-dom";
import { useState } from 'react';

function App() {
  const [current, setCurrent] = useState('')
  const menus = router.routes.map(item => (
    <Link 
      key={item.name}
      className={current === item.name ? 'active' : ''} 
      to={item.path}
      target={item.external ? "_blank" : "_self"}
      onClick={() => setCurrent(item.name)}
    >{item.name}</Link>
  ))
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
        Hello React.js
        </p>
        <div className="nav">{menus}</div>
      </header>
    </div>
  );
}

export default App;
