import { combineReducers } from 'redux';

import paymentTypes from './payment-types/reducer.js';
import registers from './registers/reducer.js';
import { setFieldReducer } from '../../tools/reducerComponents';

export default combineReducers({
	paymentTypes,
	registers,
	open: setFieldReducer([
		'REGISTER_OPEN_FETCH_SUCCESS',
	], false, 'isOpen'),
});
