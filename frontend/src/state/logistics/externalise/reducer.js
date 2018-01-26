import { combineReducers } from 'redux';
import { setFieldReducer, booleanControlReducer } from '../../../tools/reducerComponents';
import { FETCH_ALL_ACTION, FETCH_ALL_FINALLY, FETCH_ALL_ERROR, FETCH_ALL_SUCCESS } from "./actions";

export default combineReducers({
	externalisations: setFieldReducer([
		FETCH_ALL_SUCCESS,
	], [], 'externalisations'),
	loading: booleanControlReducer({
		[FETCH_ALL_ACTION]: true,
		[FETCH_ALL_FINALLY]: false,
	}, false),
	populated: booleanControlReducer({
		[FETCH_ALL_SUCCESS]: true,
	}, false),
	error: setFieldReducer([
		FETCH_ALL_ERROR,
	], null, 'reason'),
});
