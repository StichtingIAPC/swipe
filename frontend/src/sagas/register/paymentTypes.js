import { call, put } from "redux-saga/effects";
import { push } from "react-router-redux";
import { get, post, put as api_put } from "../../api";
import {
	startFetchingPaymentTypes,
	doneFetchingPaymentTypes,
	paymentTypeFetchError,
	paymentTypeInputError
} from "../../actions/register/paymentTypes";

export function* fetchPaymentTypes({ redirectTo } = {}) {
	try {
		const data = yield (yield call(
			get,
			'/register/paymenttype/',
		)).json();
		yield put(doneFetchingPaymentTypes(data));
		if (redirectTo) {
			yield put(push(redirectTo));
		}
	}	catch (e) {
		yield put(paymentTypeFetchError(e.message));
	}
}

export function* createPaymentType({ paymentType } = {}) {
	const document = { ...paymentType };

	try {
		const data = yield (yield call(
			post,
			'/register/paymenttype/',
			document,
		)).json();

		yield put(startFetchingPaymentTypes({
			redirectTo: `/register/paymenttype/${data.id}/`,
		}));
	} catch (e) {
		let msg;
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = e.json();
		yield put(paymentTypeInputError(msg));
	}
}

export function* updatePaymentType({ paymentType } = {}) {
	const document = { ...paymentType };

	try {
		const data = yield (yield call(
			api_put,
			`/register/paymenttype/${paymentType.id}/`,
			document,
		)).json();

		yield put(startFetchingPaymentTypes({
			redirectTo: `/register/paymenttype/${data.id}/`,
		}));
	} catch (e) {
		let msg;
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = e.json();
		yield put(paymentTypeInputError(msg));
	}
}
