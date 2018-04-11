/**
 * Created by nander on 16-1-18.
 */
import { getPaymentTypeIdForString } from '../../register/payment-types/selectors';
export const getPaymentTypes = state => state.register.paymentTypes.paymentTypes;
export const getPaymentsOnReceipt = state => (state.sales.payments.paymentTypes);
export const getPaymentsOnReceiptAsList = state => Object.keys(getPaymentsOnReceipt(state))
	.map(a => ({
		money: { ...getPaymentsOnReceipt(state)[a] },
		payment_type: getPaymentTypeIdForString(state, a),
	}))
	.filter(it => it.money.amount !== 0 || it.money.amount !== '0');
export const getIsPaymentSplit = state => state.sales.payments.paymentIsSplit;
