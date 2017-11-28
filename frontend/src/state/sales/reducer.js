import { combineReducers } from 'redux';

import stock from './stock/reducer.js';
import sales from './sales/reducer.js';

export default combineReducers({
	stock,
	sales,
});
