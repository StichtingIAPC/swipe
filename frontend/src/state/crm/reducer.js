import { combineReducers } from 'redux';
import { booleanControlReducer, setFieldReducer } from '../../tools/reducerComponents';
import {
	FETCH_CUSTOMERS_ACTION,
	FETCH_CUSTOMERS_SUCCESS,
	FETCH_CUSTOMERS_ERROR,
	FETCH_CUSTOMERS_FINALLY,
	FETCH_CUSTOMERS_IS_LOADING,
} from './actions';



const dataReducer = setFieldReducer([
	FETCH_CUSTOMERS_SUCCESS,
], [], 'customers');
const isLoading = booleanControlReducer({
	[FETCH_CUSTOMERS_IS_LOADING]: true,
	[FETCH_CUSTOMERS_FINALLY]: false,
}, false);

const isPopulated = booleanControlReducer({
	[FETCH_CUSTOMERS_SUCCESS]: true,
}, false);
const error = setFieldReducer([
	FETCH_CUSTOMERS_ERROR,
], null, 'reason');

export default combineReducers({
	customers: dataReducer,

});

