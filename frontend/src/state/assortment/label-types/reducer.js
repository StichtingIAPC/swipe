import { combineReducers } from 'redux';
import { booleanControlReducer, objectControlReducer, setFieldReducer } from '../../../tools/reducerComponents';

const defaultLabelType = {};

export default combineReducers({
	labelTypes: setFieldReducer([
		'assortment/label-types/FETCH_ALL_DONE',
	], [], 'labelTypes'),
	activeObject: objectControlReducer([
		'assortment/label-types/SET_FIELD',
	], defaultLabelType),
	loading: booleanControlReducer({
		'assortment/label-types/FETCH_ALL': true,
		'assortment/label-types/FETCH_ALL_FINALLY': false,
	}, false),
	populated: booleanControlReducer({
		'assortment/label-types/FETCH_ALL_DONE': true,
	}, false),
	error: setFieldReducer([
		'assortment/label-types/FETCH_ALL_FAILED',
		'assortment/label-types/FETCH_FAILED',
		'assortment/label-types/CREATE_FAILED',
		'assortment/label-types/UPDATE_FAILED',
		'assortment/label-types/DELETE_FAILED',
	], null, 'reason'),
});
