import { call, put, takeEvery, takeLatest } from 'redux-saga/effects';
import { push } from 'react-router-redux';
import * as api from './api';
import {
	doneFetchingPaymentTypes,
	paymentTypeFetchError,
	paymentTypeInputError,
	startFetchingPaymentTypes,
} from './actions';

function* fetchPaymentTypes({ redirectTo } = {}) {
	let msg = null;

	try {
		const data = yield (yield call(api.getAll)).json();

		yield put(doneFetchingPaymentTypes(data));
		if (redirectTo) {
			yield put(push(redirectTo));
		}
	}	catch (e) {
		if (e instanceof Error) {
			msg = e.message;
		}
		if (e instanceof Response) {
			msg = e.json();
		}

		yield put(paymentTypeFetchError(msg));
	}
}

function* createPaymentType({ paymentType } = {}) {
	const document = { ...paymentType };
	let msg = null;

	try {
		const data = yield (yield call(api.post, document)).json();

		yield put(startFetchingPaymentTypes({ redirectTo: `/register/paymenttype/${data.id}/` }));
	} catch (e) {
		if (e instanceof Error) {
			msg = e.message;
		}
		if (e instanceof Response) {
			msg = e.json();
		}

		yield put(paymentTypeInputError(msg));
	}
}

function* updatePaymentType({ paymentType } = {}) {
	const document = { ...paymentType };
	let msg = null;

	try {
		const data = yield (yield call(api.put, document)).json();

		yield put(startFetchingPaymentTypes({ redirectTo: `/register/paymenttype/${data.id}/` }));
	} catch (e) {
		if (e instanceof Error) {
			msg = e.message;
		}
		if (e instanceof Response) {
			msg = e.json();
		}

		yield put(paymentTypeInputError(msg));
	}
}

export default function* saga() {
	yield takeLatest('PAYMENT_TYPE_FETCH_START', fetchPaymentTypes);
	yield takeEvery('PAYMENT_TYPE_CREATE', createPaymentType);
	yield takeEvery('PAYMENT_TYPE_UPDATE', updatePaymentType);
	yield takeEvery('PAYMENT_TYPE_DELETE', updatePaymentType);
}
