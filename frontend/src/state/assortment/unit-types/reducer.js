import { combineReducers } from 'redux';
import { booleanControlReducer, objectControlReducer, setFieldReducer } from '../../../tools/reducerComponents';

const defaultUnitType = {};

export default combineReducers({
	unitTypes: setFieldReducer([
		'assortment/unit-types/FETCH_ALL_DONE',
	], [], 'unitTypes'),
	activeObject: objectControlReducer([
		'assortment/unit-types/SET_FIELD',
	], defaultUnitType),
	loading: booleanControlReducer({
		'assortment/unit-types/FETCH_ALL': true,
		'assortment/unit-types/FETCH_ALL_FINALLY': false,
	}, false),
	populated: booleanControlReducer({
		'assortment/unit-types/FETCH_ALL_DONE': true,
	}, false),
	error: setFieldReducer([
		'assortment/unit-types/FETCH_ALL_FAILED',
		'assortment/unit-types/FETCH_FAILED',
		'assortment/unit-types/CREATE_FAILED',
		'assortment/unit-types/UPDATE_FAILED',
		'assortment/unit-types/DELETE_FAILED',
	], null, 'reason'),
});
