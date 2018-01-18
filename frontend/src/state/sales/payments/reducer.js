/* eslint-disable no-undefined */
import { ADD_PAYMENT_TYPE_TO_RECEIPT, REMOVE_PAYMENT_TYPE_FROM_RECEIPT } from './actions';
const initialState = {};

export default function payments(state = initialState, action) {
	if (action.type === ADD_PAYMENT_TYPE_TO_RECEIPT) {
		return { ...state, [action.paymentType]: action.amount };
	}
	if (action.type === REMOVE_PAYMENT_TYPE_FROM_RECEIPT) {
		return { ...state, [action.paymentType]: undefined };
	}
	return state;
}
