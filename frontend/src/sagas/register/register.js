import { takeEvery } from 'redux-saga';
import { takeLatest } from 'redux-saga/effects';
import { createRegister, fetchRegisters, updateRegister } from './registers';
import { createPaymentType, fetchPaymentTypes, updatePaymentType } from './paymentTypes';
import { fetchClosedRegisterCounts, fetchOpenRegisterCounts } from './registerCounts';

export default function* registerSagas() {
	// Register sagas
	yield takeLatest('REGISTER_FETCH_START', fetchRegisters);
	yield takeEvery('REGISTER_CREATE', createRegister);
	yield takeEvery('REGISTER_UPDATE', updateRegister);
	yield takeEvery('REGISTER_DELETE', updateRegister);
	// Payment type sagas
	yield takeLatest('PAYMENT_TYPE_FETCH_START', fetchPaymentTypes);
	yield takeEvery('PAYMENT_TYPE_CREATE', createPaymentType);
	yield takeEvery('PAYMENT_TYPE_UPDATE', updatePaymentType);
	yield takeEvery('PAYMENT_TYPE_DELETE', updatePaymentType);

	yield takeLatest('REGISTERCOUNT_FETCH_OPEN_REGISTERCOUNTS', fetchOpenRegisterCounts);
	yield takeLatest('REGISTERCOUNT_FETCH_CLOSED_REGISTERCOUNTS', fetchClosedRegisterCounts);
}
