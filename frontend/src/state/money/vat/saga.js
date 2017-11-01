import { call, put, takeEvery, takeLatest } from 'redux-saga/effects';
import { push } from 'react-router-redux';
import { doneFetchingVATs, startFetchingVATs, VATFetchError, VATInputError } from './actions';
import { get, post, put as api_put } from '../../../api.js';

const format_date = date => {
	if (date)		{ return date instanceof Object ? date.format('YYYY-MM-DD') : date; }
	return null;
};

function* fetchVATs({ redirectTo }) {
	let msg = null;

	try {
		const data = yield (yield call(
			get,
			'/money/vat/',
		)).json();

		yield put(doneFetchingVATs(data));
		if (redirectTo) {
			yield put(push(redirectTo));
		}
	} catch (e) {
		if (e instanceof Error) {
			msg = e.message;
		}
		if (e instanceof Response) {
			msg = e.json();
		}

		yield put(VATFetchError(msg));
	}
}

function* createVAT({ vat }) {
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
		if (e instanceof Error) {
			msg = e.message;
		}
		if (e instanceof Response) {
			msg = yield e.json();
		}

		yield put(VATInputError(msg));
	}
}

function* updateVAT({ vat }) {
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
		if (e instanceof Error) {
			msg = e.message;
		}
		if (e instanceof Response) {
			msg = yield e.json();
		}

		yield put(VATInputError(msg));
	}
}

export default function* saga() {
	yield takeLatest('VAT_FETCH_START', fetchVATs);
	yield takeEvery('VAT_CREATE', createVAT);
	yield takeEvery('VAT_UPDATE', updateVAT);
}
