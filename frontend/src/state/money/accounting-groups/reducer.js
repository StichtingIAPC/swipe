import { combineReducers } from 'redux';
import {
	booleanControlReducer,
	collectReducers, objectControlReducer, resetFieldReducer,
	setFieldReducer,
} from '../../../tools/reducerComponents';

const defaultAccountingGroup = {
	id: null,
	name: '',
	accounting_number: null,
	vat_group: null,
};

export default combineReducers({
	accountingGroups: setFieldReducer([
		'money/accounting-groups/FETCH_ALL_DONE',
	], [], 'accountingGroups'),
	activeObject: collectReducers(
		resetFieldReducer([
			'money/accounting-groups/NEW_ACCOUNTINGGROUP',
		], defaultAccountingGroup),
		objectControlReducer([
			'money/accounting-groups/SET_FIELD',
		], defaultAccountingGroup),
		setFieldReducer([
			'money/accounting-groups/FETCH_DONE',
		], defaultAccountingGroup, 'accountingGroup')
	),
	loading: booleanControlReducer({
		'money/accounting-groups/FETCH_ALL': true,
		'money/accounting-groups/FETCH_ALL_FINALLY': false,
	}, false),
	populated: booleanControlReducer({
		'money/accounting-groups/FETCH_ALL_DONE': true,
	}, false),
	error: setFieldReducer([
		'money/accounting-groups/FETCH_ALL_FAILED',
		'money/accounting-groups/FETCH_FAILED',
		'money/accounting-groups/CREATE_FAILED',
		'money/accounting-groups/UPDATE_FAILED',
		'money/accounting-groups/DELETE_FAILED',
	], null, 'reason'),
});
