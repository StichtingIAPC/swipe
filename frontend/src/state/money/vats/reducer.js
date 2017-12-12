import { combineReducers } from 'redux';
import {
	booleanControlReducer,
	collectReducers, objectControlReducer, resetFieldReducer,
	setFieldReducer,
} from '../../../tools/reducerComponents';

const defaultvat = {
	id: null,
	name: '',
	active: true,
	vatperiod_set: [],
};

export default combineReducers({
	vats: setFieldReducer([
		'money/vats/FETCH_ALL_DONE',
	], [], 'vats'),
	activeObject: collectReducers(
		resetFieldReducer([
			'money/vats/NEW_VAT',
		], defaultvat),
		objectControlReducer([
			'money/vats/SET_FIELD',
		], defaultvat),
		setFieldReducer([
			'money/vats/FETCH_DONE',
		], defaultvat, 'vat')
	),
	loading: booleanControlReducer({
		'money/vats/FETCH_ALL': true,
		'money/vats/FETCH_ALL_FINALLY': false,
	}, false),
	populated: booleanControlReducer({
		'money/vats/FETCH_ALL_DONE': true,
	}, false),
	error: setFieldReducer([
		'money/vats/FETCH_ALL_FAILED',
		'money/vats/FETCH_FAILED',
		'money/vats/CREATE_FAILED',
		'money/vats/UPDATE_FAILED',
		'money/vats/DELETE_FAILED',
	], null, 'reason'),
});
