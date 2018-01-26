import { call, put, takeEvery, takeLatest } from 'redux-saga/effects';

import * as api from '../../../api';
import * as actions from './actions.js';
import { FETCH_ALL_ACTION } from './actions';

export function* fetchAll() {
	try {
		const externalizations = yield (yield call(
			api.get,
			'/externalise/',
		)).json();

		const exts = [].concat.apply([], externalizations.map(e => e.externaliseline_set.map(en => ({
			memo: e.memo,
			count: en.count,
			amount: en.cost.amount,
			article: en.article_type,
		}))));

		yield put(actions.fetchAllSuccess(exts));
	} catch (e) {
		console.log(e);
		yield put(actions.fetchAllError(e));
	} finally {
		yield put(actions.fetchAllFinally());
	}
}

export default function* saga() {
	yield takeLatest(FETCH_ALL_ACTION, fetchAll);
}
