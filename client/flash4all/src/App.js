import React from 'react';
import logo from './logo.svg';
import TokenList from './components/TokenList';
import { Home } from './pages';
import './App.css';
import Web3 from 'web3';

import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";

function App() {

  return (
    <div className="App">
      <Router>
        <div>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
          </ul>

          <Switch>
            <Route path="/">
              <Home />
            </Route>
          </Switch>
        </div>
      </Router>
    </div>
  );
}

export default App;
