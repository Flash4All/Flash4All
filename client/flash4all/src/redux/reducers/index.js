import { combineReducers } from 'redux';
import tokenReducer from './tokenReducer';
import tradingPairReducer from './tradingPairReducer';

export const reducer = combineReducers({
  token: tokenReducer,
  tradingPair: tradingPairReducer,
});

