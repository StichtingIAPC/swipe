import { combineReducers } from 'redux';
import {
	setFieldReducer,
	booleanControlReducer,
	objectControlReducer,
	resetFieldReducer, collectReducers, pathControlReducer
} from '../../../tools/reducerComponents';
import {
	FETCH_ALL_ACTION,
	FETCH_ALL_FINALLY,
	FETCH_ALL_ERROR,
	FETCH_ALL_SUCCESS,
	NEW_ACTION,
	SET_FIELD_ACTION,
	CREATE_SUCCESS, SET_VALIDATIONS
} from './actions';

const defaultExternalisation = {
	id: null,
	externaliseline_set: [],
};

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
	activeObject: collectReducers(
		resetFieldReducer([
			NEW_ACTION,
			CREATE_SUCCESS,
		], defaultExternalisation),
		pathControlReducer([
			SET_FIELD_ACTION,
		], defaultExternalisation),
	),
	validations: setFieldReducer([
		SET_VALIDATIONS,
	], {}, 'validations'),
	error: setFieldReducer([
		FETCH_ALL_ERROR,
	], null, 'reason'),
});
