import { call, put, takeEvery, takeLatest } from 'redux-saga/effects';
import { push } from 'react-router-redux';
import { get, post, put as api_put } from '../../../api.js';
import {
	doneFetchingPaymentTypes,
	paymentTypeFetchError,
	paymentTypeInputError,
	startFetchingPaymentTypes,
} from './actions';

function* fetchPaymentTypes({ redirectTo } = {}) {
	let msg = null;

	try {
		const data = yield (yield call(
			get,
			'/register/paymenttypes/',
		)).json();

		yield put(doneFetchingPaymentTypes(data));
		if (redirectTo)
			yield put(push(redirectTo));
	}	catch (e) {
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = e.json();

		yield put(paymentTypeFetchError(msg));
	}
}

function* createPaymentType({ paymentType } = {}) {
	const document = { ...paymentType };
	let msg = null;

	try {
		const data = yield (yield call(
			post,
			'/register/paymenttypes/',
			document,
		)).json();

		yield put(startFetchingPaymentTypes({ redirectTo: `/register/paymenttype/${data.id}/` }));
	} catch (e) {
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = e.json();

		yield put(paymentTypeInputError(msg));
	}
}

function* updatePaymentType({ paymentType } = {}) {
	const document = { ...paymentType };
	let msg = null;

	try {
		const data = yield (yield call(
			api_put,
			`/register/paymenttypes/${paymentType.id}/`,
			document,
		)).json();

		yield put(startFetchingPaymentTypes({ redirectTo: `/register/paymenttype/${data.id}/` }));
	} catch (e) {
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = e.json();

		yield put(paymentTypeInputError(msg));
	}
}

export default function* saga() {
	yield takeLatest('PAYMENT_TYPE_FETCH_START', fetchPaymentTypes);
	yield takeEvery('PAYMENT_TYPE_CREATE', createPaymentType);
	yield takeEvery('PAYMENT_TYPE_UPDATE', updatePaymentType);
	yield takeEvery('PAYMENT_TYPE_DELETE', updatePaymentType);
}
