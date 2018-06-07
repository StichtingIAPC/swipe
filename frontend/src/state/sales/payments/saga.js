import { validate, validator } from '../../../tools/validations/validators';
import { getPaymentsOnReceiptDeficit, getIsPaymentSplit } from './selectors';
import { put, select, takeLatest } from 'redux-saga/effects';
import * as actions from './actions';
import Big from 'big.js';

const validations = [
	validator('total', 'Total', a => {
		const totalBig = new Big(a.total);

		if (!a.isSplit || totalBig.eq(0)) {
			return null;
		}
		return () => ({
			type: 'error',
			text: `Split amount does not add up to total. ${totalBig > 0 ? 'Deficit' : 'Excess'}: ${totalBig.abs()}`,
		});
	}),
];

export function* splitPaymentTypeValidator() {
	const current = yield select(getPaymentsOnReceiptDeficit);
	const isSplit = yield select(getIsPaymentSplit);
	const res = validate({ total: {
		total: current,
		isSplit,
	}}, validations);

	yield put(actions.setValidations(res));
}

export default function* saga() {
	yield takeLatest(actions.SET_AMOUNT_OF_PAYMENT_TYPE_ON_RECEIPT, splitPaymentTypeValidator);
	yield takeLatest(actions.RESET_AMOUNTS_OF_PAYMENT_TYPES_ON_RECEIPT, splitPaymentTypeValidator);
}
