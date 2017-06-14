import { combineReducers } from "redux";
import { booleanField, replaceField, reSetField } from "../tools/subReducers";

export default combineReducers({
	paymentTypes: replaceField('PAYMENT_TYPE_FETCH_DONE', [], 'paymentTypes'),
	fetching: booleanField({
		PAYMENT_TYPE_FETCH_START: true,
		PAYMENT_TYPE_FETCH_DONE: false,
		PAYMENT_TYPE_FETCH_ERROR: false,
	}, false),
	fetchError: reSetField('PAYMENT_TYPE_FETCH_ERROR', 'PAYMENT_TYPE_FETCH_DONE', null, 'error'),
	inputError: reSetField('PAYMENT_TYPE_INPUT_ERROR', 'PAYMENT_TYPE_FETCH_START', null, 'error'),
	populated: booleanField({ PAYMENT_TYPE_FETCH_DONE: true }, false),
});
