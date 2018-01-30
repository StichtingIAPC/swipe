/**
 * Created by nander on 16-1-18.
 */
import {getPaymentTypeIdForString} from "../../register/payment-types/selectors";
export const getPaymentTypes = state => state.register.paymentTypes.paymentTypes;
export const getPaymentsOnReceipt = state => state.sales.payments;
export const getPaymentsOnReceiptAsList = (state) => {
	return Object.keys(state.sales.payments).map((a) => ({ money: { ...state.sales.payments[a] }, payment_type: getPaymentTypeIdForString(state, a) })).filter(it=>it.money.amount != 0);
};
