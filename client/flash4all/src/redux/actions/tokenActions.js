import axios from 'axios';
import { TOKEN_TYPES } from '../types';
const API=process.env.REACT_APP_API_ENDPOINT;

let { TOKENS_RECEIVED, TOKEN_ADDED, ARBITRAGE_RECEIVED } = TOKEN_TYPES;

const arbitrage = (token) => {
  return (dispatch) => {
    return axios.post(`${API}/arbitrage`, { token })
      .then((response) => {
        return dispatch({type: ARBITRAGE_RECEIVED, payload: response.data});
      })
      .catch((err) => {
        console.log(err);
      });
  };
};

const fetchTokens = () => {
  return (dispatch) => {
    return axios.get(`https://flash4all.net/api/tokens`)
      .then((response) => {
        return dispatch({type: TOKENS_RECEIVED, payload: response.data});
      })
      .catch((err) => {
        console.log(err);
      });
  };
};

const addToken = (token) => {
  return (dispatch) => {
    return axios.post(`${API}/tokens`, {token})
      .then((response) => {
        return dispatch({type: TOKEN_ADDED, payload: response.data});
      })
      .catch((err) => {
        console.log(err);
      });
  };
};

export default {
  fetchTokens,
  addToken,
  arbitrage,
};
