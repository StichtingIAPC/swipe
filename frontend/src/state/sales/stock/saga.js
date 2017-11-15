import { call, put, takeEvery, takeLatest } from 'redux-saga/effects';
import { push } from 'react-router-redux';
import { get, post, put as api_put } from '../../../api.js';
import {doneFetchingStockList, fetchingStockListError} from "./actions";

function* fetchStock({ redirectTo } = {}) {
	let msg = null;
	console.log("PENIS");
	try {
		const data = yield (yield call(
			get,
			'/stock/',
		)).json();

		yield put(doneFetchingStockList(data));
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
		yield put(fetchingStockListError(msg));
	}
}

export default function* stockSaga() {
	yield takeLatest('STOCK_FETCH_START', fetchStock);
}
