import { TOKEN_TYPES } from '../types';

const initialState = {
  tokens: [],
  trades: [],
};

let { TOKENS_RECEIVED, TOKEN_ADDED, ARBITRAGE_RECEIVED } = TOKEN_TYPES;

export default (state = initialState, action) => {
  switch (action.type) {
    case TOKENS_RECEIVED:
      return {...state, tokens: action.payload.tokens || action.payload};
    case ARBITRAGE_RECEIVED:
      return {...state, trades: action.payload.result || action.payload};
    case TOKEN_ADDED:
      let newToken = action.payload.token || action.payload
      return {...state, tokens: [...state.tokens, newToken]};
    default:
      return state;
  }
};

