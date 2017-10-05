import { call, put } from 'redux-saga/effects';
import { push } from 'react-router-redux';
import { get, post, put as api_put } from '../../api';
import {
	doneFetchingPaymentTypes,
	paymentTypeFetchError,
	paymentTypeInputError,
	startFetchingPaymentTypes,
} from '../../actions/register/paymentTypes';

export function* fetchPaymentTypes({ redirectTo } = {}) {
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

export function* createPaymentType({ paymentType } = {}) {
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

export function* updatePaymentType({ paymentType } = {}) {
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
