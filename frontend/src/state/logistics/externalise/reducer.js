import { combineReducers } from 'redux';
import {
	setFieldReducer,
	booleanControlReducer,
	resetFieldReducer,
	collectReducers,
	pathControlReducer,
} from '../../../tools/reducerComponents';
import {
	LOGISTICS_EXTRNALIZE_FETCH_ALL_FINALLY,
	LOGISTICS_EXTRNALIZE_FETCH_ALL_FAIL,
	LOGISTICS_EXTRNALIZE_FETCH_ALL_SUCCESS,
	LOGISTICS_EXTRNALIZE_NEW,
	LOGISTICS_EXTRNALIZE_SET_FIELD,
	LOGISTICS_EXTRNALIZE_CREATE_SUCCESS,
	LOGISTICS_EXTRNALIZE_SET_VALIDATIONS,
	LOGISTICS_EXTRNALIZE_SET_LOADING,
} from './actions';

const defaultExternalisation = {
	id: null,
	memo: '',
	externaliseline_set: [],
};

export default combineReducers({
	externalisations: setFieldReducer([
		LOGISTICS_EXTRNALIZE_FETCH_ALL_SUCCESS,
	], [], 'externalisations'),
	isLoading: booleanControlReducer({
		[LOGISTICS_EXTRNALIZE_SET_LOADING]: true,
		[LOGISTICS_EXTRNALIZE_FETCH_ALL_FINALLY]: false,
	}, false),
	isPopulated: booleanControlReducer({
		[LOGISTICS_EXTRNALIZE_FETCH_ALL_SUCCESS]: true,
	}, false),
	error: setFieldReducer([
		LOGISTICS_EXTRNALIZE_FETCH_ALL_FAIL,
	], null, 'reason'),

	activeObject: collectReducers(
		resetFieldReducer([
			LOGISTICS_EXTRNALIZE_NEW,
			LOGISTICS_EXTRNALIZE_CREATE_SUCCESS,
		], defaultExternalisation),
		pathControlReducer([
			LOGISTICS_EXTRNALIZE_SET_FIELD,
		], defaultExternalisation),
	),
	validations: setFieldReducer([
		LOGISTICS_EXTRNALIZE_SET_VALIDATIONS,
	], {}, 'validations'),
});
