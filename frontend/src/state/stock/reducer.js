import { STOCK_FETCH_DONE, STOCK_FETCH_FAILED, STOCK_FETCH_ACTION } from './actions';
import {
	booleanControlReducer, collectReducers, resetFieldReducer,
	setFieldReducer
} from '../../tools/reducerComponents';
import { combineReducers } from 'redux';


export default combineReducers({
	stock: setFieldReducer([ STOCK_FETCH_DONE ], [], 'stock'),
	loading: booleanControlReducer({
		[STOCK_FETCH_ACTION]: true,
		[STOCK_FETCH_DONE]: false,
		[STOCK_FETCH_FAILED]: false }, false),
	populated: booleanControlReducer({[STOCK_FETCH_ACTION]: false,
		[STOCK_FETCH_DONE]: true,
	}, false),
	fetchError: collectReducers(resetFieldReducer([ STOCK_FETCH_DONE ], null), setFieldReducer([ STOCK_FETCH_FAILED ], null, 'error')),
});
