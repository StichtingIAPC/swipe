import { combineReducers } from 'redux';

import sales from './sales/reducer.js';
import payments from './payments/reducer.js';

export default combineReducers({
	sales,
	payments,
});
