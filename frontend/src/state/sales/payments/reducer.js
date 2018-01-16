/* eslint-disable no-undefined */
import {ADD_PAYMENT_TYPE, REMOVE_PAYMENT_TYPE} from "./actions";
const initialState = {};

export default function payments(state = initialState, action) {
	if (action.type === ADD_PAYMENT_TYPE){
		return { ...state, [action.paymentType]: action.amount };
	}
	if (action.type === REMOVE_PAYMENT_TYPE){
		return { ...state, [action.paymentType]: undefined };
	}
	return state;
}