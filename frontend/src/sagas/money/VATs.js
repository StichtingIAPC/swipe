import { call, put } from 'redux-saga/effects';
import { push } from 'react-router-redux';
import { doneFetchingVATs, startFetchingVATs, VATFetchError, VATInputError } from '../../actions/money/VATs';
import { get, post, put as api_put } from '../../api';

const format_date = date => {
	if (date)
		return date instanceof Object ? date.format('YYYY-MM-DD') : date;
	return null;
};

export function* fetchVATs({ redirectTo }) {
	let msg = null;

	try {
		const data = yield (yield call(
			get,
			'/money/vat/',
		)).json();

		yield put(doneFetchingVATs(data));
		if (redirectTo)
			yield put(push(redirectTo));
	} catch (e) {
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = e.json();

		yield put(VATFetchError(msg));
	}
}

export function* createVAT({ vat }) {
	const VAT = {
		...vat,
		vatperiod_set: vat.vatperiod_set.map(
			vp => ({
				...vp,
				begin_date: format_date(vp.begin_date),
				end_date: format_date(vp.end_date),
			})
		),
	};
	let msg = null;

	try {
		const data = yield (yield call(
			post,
			'/money/vat/',
			VAT,
		)).json();

		yield put(startFetchingVATs({ redirectTo: `/money/vat/${data.id}/` }));
	} catch (e) {
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = yield e.json();

		yield put(VATInputError(msg));
	}
}

export function* updateVAT({ vat }) {
	const VAT = {
		...vat,
		vatperiod_set: vat.vatperiod_set.map(
			vp => ({
				...vp,
				begin_date: format_date(vp.begin_date),
				end_date: format_date(vp.end_date),
			})
		),
	};
	let msg = null;

	try {
		const data = yield (yield call(
			api_put,
			`/money/vat/${VAT.id}/`,
			VAT,
		)).json();

		yield put(startFetchingVATs({ redirectTo: `/money/vat/${data.id}/` }));
	} catch (e) {
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = yield e.json();

		yield put(VATInputError(msg));
	}
}
