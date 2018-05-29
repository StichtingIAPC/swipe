/* eslint-disable no-undefined */
import {
	RESET_AMOUNTS_OF_PAYMENT_TYPES_ON_RECEIPT,
	SET_AMOUNT_OF_PAYMENT_TYPE_ON_RECEIPT,
	SET_VALIDATIONS,
	TOGGLE_SPLIT_PAYMENT
} from './actions';
import {
	booleanControlReducer, collectReducers, objectControlReducer,
	resetFieldReducer, setFieldReducer
} from '../../../tools/reducerComponents';
import { combineReducers } from 'redux';

export default combineReducers({
	paymentTypes: collectReducers(
		objectControlReducer(
			[ SET_AMOUNT_OF_PAYMENT_TYPE_ON_RECEIPT ],
			{}
		),
		resetFieldReducer(
			[ RESET_AMOUNTS_OF_PAYMENT_TYPES_ON_RECEIPT ],
			{}
		)),
	paymentIsSplit: booleanControlReducer({
		[TOGGLE_SPLIT_PAYMENT]: 'toggle',
	},
	false),
	validations: setFieldReducer([
		SET_VALIDATIONS,
	], {}, 'validations'),
});
