import { combineReducers } from 'redux';

import paymentTypes from './payment-types/reducer.js';
import registers from './registers/reducer.js';

export default combineReducers({
	paymentTypes,
	registers,
});
