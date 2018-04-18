import { STOCK_FETCH_DONE, STOCK_FETCH_FAIL, STOCK_FETCH_START } from './actions';
import {
	booleanControlReducer, collectReducers, resetFieldReducer,
	setFieldReducer
} from '../../tools/reducerComponents';
import { combineReducers } from 'redux';


export default combineReducers({
	stock: setFieldReducer([ STOCK_FETCH_DONE ], [], 'stock'),
	fetching: booleanControlReducer({
		[STOCK_FETCH_START]: true,
		[STOCK_FETCH_DONE]: false,
		[STOCK_FETCH_FAIL]: false }, false),
	fetchError: collectReducers(resetFieldReducer([ STOCK_FETCH_DONE ], null), setFieldReducer([ STOCK_FETCH_FAIL ], null, 'error')),
});
