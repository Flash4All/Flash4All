import axios from 'axios';
import { TOKENS_RECEIVED } from '../types';

const API=process.env.REACT_APP_API_ENDPOINT;

const getTokens = () => {
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


export default {
  getTokens
};
