import { TRADING_PAIR_TYPES } from '../types';

const initialState = {
  tradingPairs: [],
};

export default (state = initialState, action) => {
  switch (action.type) {
    case TRADING_PAIR_TYPES.TRADING_PAIR_RECEIVED:
      return {...state, tokens: action.payload.tradingPair || action.payload};
    default:
      return state;
  }
};
