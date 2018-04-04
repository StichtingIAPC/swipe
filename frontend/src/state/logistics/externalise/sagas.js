import { call, put, takeEvery, takeLatest } from 'redux-saga/effects';
import { push } from 'react-router-redux';
import store from '../../store';

import * as api from './api';
import * as actions from './actions';
import { cleanErrorMessage } from '../../../tools/sagaHelpers';

export function* fetchAll() {
	try {
		const externalizations = yield (yield call(api.getAll)).json();

		const exts = [].concat.apply([], externalizations.map(e => e.externaliseline_set.map(en => ({
			memo: e.memo,
			count: en.count,
			amount: en.cost,
			article: en.article_type,
		}))));

		yield put(actions.fetchAllSuccess(exts));
	} catch (e) {
		console.error(e);
		yield put(actions.fetchAllError(e));
	} finally {
		yield put(actions.fetchAllFinally());
	}
}

export function* create({ externalise }) {
	const document = {
		externaliseline_set: externalise.externaliseline_set.map(e => ({
			...e,
			// eslint-disable-next-line
			amount: undefined,
			cost: e.amount,
			article: e.article.id,
		})),
		memo: externalise.memo,
		user: store.getState().auth.currentUser.id,
	};

	try {
		const newExternalise = yield (yield call(api.post, document)).json();

		yield put(actions.createSuccess(newExternalise));
	} catch (e) {
		yield put(actions.createError(cleanErrorMessage(e)));
	} finally {
		yield put(actions.createFinally());
	}
}

export function* createSuccess() {
	yield put(actions.fetchAllAction());
	yield put(push('/logistics/externalise'));
}

export default function* saga() {
	yield takeLatest(actions.FETCH_ALL_ACTION, fetchAll);
	yield takeEvery(actions.CREATE_ACTION, create);
	yield takeLatest(actions.CREATE_SUCCESS, createSuccess);
}
