import React from 'react'
import ReactDOM from 'react-dom'
import * as serviceWorker from './serviceWorker';
import { Provider } from 'react-redux'
import App from './App'
import { initStore } from './redux';
import {applyMiddleware, createStore} from "redux";
//import {Router, Route, browserHistory} from "react-router";
//import {syncHistoryWithStore} from "react-router-redux";


const rootElement = document.getElementById('root')
const store = initStore();


ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  rootElement
)

serviceWorker.unregister();
