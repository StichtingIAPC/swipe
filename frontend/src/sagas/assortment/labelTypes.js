import { call, put } from "redux-saga/effects";
import { push } from "react-router-redux";
import { get, post, put as api_put } from "../../api";
import {
	startFetchingLabelTypes,
	doneFetchingLabelTypes,
	labelTypeFetchError,
	labelTypeInputError
} from "../../actions/assortment/labelTypes";

export function* fetchLabelTypes({redirectTo} = {}) {
	try {
		const data = yield (yield call(
			get,
			"/assortment/labeltypes/",
		)).json();
		yield put(doneFetchingLabelTypes(data));
		if (redirectTo) {
			yield put(push(redirectTo));
		}
	} catch (e) {
		let msg;
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = e.json();
		yield put(labelTypeFetchError(msg));
	}
}

export function* createLabelType({ labelType } = {}) {
	const document = { ...labelType };

	try {
		const data = yield (yield call(
			post,
			'/assortment/labeltypes/',
			document
		));

		yield put(startFetchingLabelTypes({
			redirectTo: `/assortment/labeltype/`,
		}));
	} catch (e) {
		let msg;
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = e.json();
		yield put(labelTypeInputError(msg));
	}
}

export function* updateLabelType({ labelType }) {
	const document = { ...labelType };

	try {
		const data = yield (yield call(
			api_put,
			`/assortment/labeltypes/${document.id}/`,
			document,
		)).json();
		yield put(startFetchingLabelTypes({
			redirectTo: `/assortment/labeltype/${data.id}/`,
		}));
	} catch (e) {
		let msg;
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = e.json();
		yield put(labelTypeInputError(msg));
	}
}
