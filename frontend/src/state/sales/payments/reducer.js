/* eslint-disable no-undefined */
import { SALES_PAYMENT_TYPES_ADD_TO_RECEIPT, SALES_PAYMENT_TYPE_REMOVE_FROM_RECEIPT } from './actions';
const initialState = {};

export default function payments(state = initialState, action) {
	if (action.type === SALES_PAYMENT_TYPES_ADD_TO_RECEIPT) {
		return { ...state, [action.paymentType]: action.amount };
	}
	if (action.type === SALES_PAYMENT_TYPE_REMOVE_FROM_RECEIPT) {
		return { ...state, [action.paymentType]: undefined };
	}
	return state;
}
