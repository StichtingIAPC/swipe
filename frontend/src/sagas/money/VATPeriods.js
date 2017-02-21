import { call, put } from "redux-saga/effects";
import { push } from "react-router-redux";
import {
	startFetchingVATPeriods,
	doneFetchingVATPeriods,
	VATPeriodInputError,
	VATPeriodFetchError
} from "../../actions/money/VATPeriods";
import { get, post, put as api_put } from "../../api";

export function* fetchVATPeriods({ redirectTo }) {
	try {
		const data = yield (yield call(
			get,
			'/money/vatperiod/',
		)).json();
		yield put(doneFetchingVATPeriods(data));
		if (redirectTo)
			yield put(push(redirectTo));
	} catch (e) {
		yield put(VATPeriodFetchError(e.message));
	}
}

export function* createVATPeriod({ vPeriod }) {
	const VATPeriod = {...vPeriod};
	try {
		const data = yield (yield call(
			api_put,
			'/money/vatperiod/',
			VATPeriod,
		)).json();
		yield put(startFetchingVATPeriods({
			redirectTo: `/money/vatperiod/${data.id}/`,
		}));
	} catch (e) {
		let msg;
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = yield call(e.json.bind(e));
		yield put(VATPeriodInputError(msg));
	}
}

export function* updateVATPeriod({ vPeriod }) {
	const VATPeriod = {...vPeriod};
	try {
		const data = yield (yield call(
			post,
			`/money/vatperiod/${VATPeriod.id}/`,
			VATPeriod,
		)).json();
		yield put(startFetchingVATPeriods({
			redirectTo: `/money/vatperiod/${data.id}/`,
		}));
	} catch (e) {
		let msg;
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = yield call(e.json.bind(e));
		yield put(VATPeriodInputError(msg));
	}
}
