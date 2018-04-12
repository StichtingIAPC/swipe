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
	CREATE_SUCCESS, SET_VALIDATIONS, SET_LOADING_ACTION
} from './actions';

const defaultExternalisation = {
	id: null,
	memo: '',
	externaliseline_set: [],
};

export default combineReducers({
	externalisations: setFieldReducer([
		FETCH_ALL_SUCCESS,
	], [], 'externalisations'),
	isLoading: booleanControlReducer({
		[SET_LOADING_ACTION]: true,
		[FETCH_ALL_FINALLY]: false,
	}, false),
	isPopulated: booleanControlReducer({
		[FETCH_ALL_SUCCESS]: true,
	}, false),
	error: setFieldReducer([
		FETCH_ALL_ERROR,
	], null, 'reason'),

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
});
