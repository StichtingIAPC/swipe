import { combineReducers } from 'redux';
import {
	setFieldReducer,
	resetFieldReducer,
	collectReducers,
	pathControlReducer,
} from '../../../tools/reducerComponents';
import { crudReducers, crudActions } from '../../../tools/CRUDHelper';
const {
	FETCH_ALL_FINALLY,
	FETCH_ALL_FAIL,
	FETCH_ALL_SUCCESS,
	SET_FIELD,
	CREATE_START,
	CREATE_SUCCESS,
	SET_VALIDATIONS,
	SET_LOADING,
} = crudActions('/logistics/externalize/');

const defaultExternalisation = {
	id: null,
	memo: '',
	externaliseline_set: [],
};

export default combineReducers({
	...crudReducers(),

	activeObject: collectReducers(
		resetFieldReducer([
			CREATE_START,
			CREATE_SUCCESS,
		], defaultExternalisation),
		pathControlReducer([
			SET_FIELD,
		], defaultExternalisation),
	),
	validations: setFieldReducer([
		SET_VALIDATIONS,
	], {}, 'validations'),
});
