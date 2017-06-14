import { booleanField, replaceField, reSetField } from "./tools/subReducers";
import { combineReducers } from "redux";

export default combineReducers({
	suppliers: replaceField('SUPPLIER_FETCH_DONE', [], 'suppliers'),
	fetching: booleanField({
		SUPPLIER_FETCH_START: true,
		SUPPLIER_FETCH_DONE: false,
		SUPPLIER_FETCH_ERROR: false,
	}, false),
	fetchError: reSetField('SUPPLIER_FETCH_ERROR', 'SUPPLIER_FETCH_DONE', null, 'error'),
	inputError: reSetField('SUPPLIER_INPUT_ERROR', 'SUPPLIER_FETCH_START', null, 'error'),
	populated: booleanField({ SUPPLIER_FETCH_DONE: true }, false),
});
