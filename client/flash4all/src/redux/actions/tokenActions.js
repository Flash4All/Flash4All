import axios from 'axios';
import { TOKEN_TYPES } from '../types';
const API=process.env.REACT_APP_API_ENDPOINT;

let { TOKENS_RECEIVED, TOKEN_ADDED } = TOKEN_TYPES;

const fetchTokens = () => {
  return (dispatch) => {
    return axios.get(`${API}/tokens`)
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
};
