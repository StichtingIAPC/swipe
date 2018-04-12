import { combineReducers } from 'redux';
import {
	booleanControlReducer, collectReducers, objectControlReducer,
	resetFieldReducer, setFieldReducer,
} from '../../tools/reducerComponents';
import { SET_VALIDATIONS } from './actions';

const defaultSupplier = {
	id: null,
	name: '',
	deleted: false,
	notes: '',
	search_url: '',
};

export default combineReducers({
	suppliers: setFieldReducer([
		'suppliers/FETCH_ALL_DONE',
	], [], 'suppliers'),
	activeObject: collectReducers(
		resetFieldReducer([
			'suppliers/NEW_SUPPLIER',
		], defaultSupplier),
		objectControlReducer([
			'suppliers/SET_FIELD',
		], defaultSupplier),
		setFieldReducer([
			'suppliers/FETCH_DONE',
		], defaultSupplier, 'supplier')
	),
	validations: setFieldReducer([
		SET_VALIDATIONS,
	], {}, 'validations'),
	loading: booleanControlReducer({
		'suppliers/FETCH_ALL': true,
		'suppliers/FETCH_ALL_FINALLY': false,
	}, false),
	populated: booleanControlReducer({
		'suppliers/FETCH_ALL_DONE': true,
	}, false),
	error: setFieldReducer([
		'suppliers/FETCH_ALL_FAILED',
		'suppliers/FETCH_FAILED',
		'suppliers/CREATE_FAILED',
		'suppliers/UPDATE_FAILED',
		'suppliers/DELETE_FAILED',
	], null, 'reason'),
});
