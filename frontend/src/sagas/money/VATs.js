import { call, put } from "redux-saga/effects";
import { push } from "react-router-redux";
import { startFetchingVATs, doneFetchingVATs, VATInputError, VATFetchError } from "../../actions/money/VATs";
import { get, post, put as api_put } from "../../api";

const format_date = date => date ? (date instanceof Date ? date.format('YYYY-MM-DD') : date) : null;

export function* fetchVATs({ redirectTo }) {
	try {
		const data = yield (yield call(
			get,
			'/money/vat/',
		)).json();
		yield put(doneFetchingVATs(data));
		if (redirectTo)
			yield put(push(redirectTo));
	} catch (e) {
		yield put(VATFetchError(e.message));
	}
}

export function* createVAT({ vat }) {
	const VAT = {
		...vat,
		vatperiod_set: vat.vatperiod_set.map(
			(vp) => ({
				...vp,
				begin_date: format_date(vp.begin_date),
				end_date: format_date(vp.end_date),
			})
		),
	};
	try {
		const data = yield (yield call(
			post,
			'/money/vat/',
			VAT,
		)).json();
		yield put(startFetchingVATs({
			redirectTo: `/money/vat/${data.id}/`,
		}));
	} catch (e) {
		let msg;
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = yield call(e.json.bind(e));
		yield put(VATInputError(msg));
	}
}

export function* updateVAT({ vat }) {
	const VAT = {
		...vat,
		vatperiod_set: vat.vatperiod_set.map(
			(vp) => ({
				...vp,
				begin_date: format_date(vp.begin_date),
				end_date: format_date(vp.end_date),
			})
		),
	};	try {
		const data = yield (yield call(
			api_put,
			`/money/vat/${VAT.id}/`,
			VAT,
		)).json();
		yield put(startFetchingVATs({
			redirectTo: `/money/vat/${data.id}/`,
		}));
	} catch (e) {
		let msg;
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = yield call(e.json.bind(e));
		yield put(VATInputError(msg));
	}
}
