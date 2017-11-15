import { combineReducers } from 'redux';

import stock from './stock/reducer.js';

export default combineReducers({
	stock,
});
