import { combineReducers } from 'redux';

import sales from './sales/reducer.js';
import payments from './payments/reducer.js';
import { setFieldReducer } from '../../tools/reducerComponents';
import { SET_CUSTOMER } from './actions';

export default combineReducers({
	customer: setFieldReducer([
		SET_CUSTOMER,
	], null, 'customer'),
	sales,
	payments,
});
