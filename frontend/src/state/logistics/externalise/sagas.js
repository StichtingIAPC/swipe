import { call, put, takeEvery, takeLatest, select } from 'redux-saga/effects';
import { push } from 'react-router-redux';
import store from '../../store';

import * as api from './api';
import * as actions from './actions';
import { cleanErrorMessage } from '../../../tools/sagaHelpers';
import { getExternalisationActiveObject, getExternalisationLoading, getExternalisationPopulated } from './selectors';
import { isMoney, validate, validator } from '../../../tools/validations/validators';
import { setLoadingAction } from "./actions";

export function* fetchAll () {
	if (yield select (getExternalisationLoading))
		return;
	yield put (setLoadingAction ());
	try {

		const externalizations = yield (yield call (api.getAll)).json ();

		const exts = [].concat.apply ([], externalizations.map (e => e.externaliseline_set.map (en => ({
			memo: e.memo,
			count: en.count,
			amount: en.cost,
			article: en.article_type,
		}))));

		yield put (actions.fetchAllSuccess (exts));
	} catch (e) {
		console.error (e);
		yield put (actions.fetchAllError (e));
	} finally {
		yield put (actions.fetchAllFinally ());
	}
}

export function* create ( { externalise } ) {
	const document = {
		externaliseline_set: externalise.externaliseline_set.map (e => ({
			...e,
			// eslint-disable-next-line
			amount: undefined,
			cost: e.amount,
			article: e.article.id,
		})),
		memo: externalise.memo,
		user: store.getState ().auth.currentUser.id,
	};

	try {
		const newExternalise = yield (yield call (api.post, document)).json ();

		yield put (actions.createSuccess (newExternalise));
	} catch (e) {
		yield put (actions.createError (cleanErrorMessage (e)));
	} finally {
		yield put (actions.createFinally ());
	}
}

export function* createSuccess () {
	yield put (actions.fetchAllAction ());
	yield put (push ('/logistics/externalise'));
}

const validations = [
	validator ('memo', 'Memo', memo => memo.length > 3 ? null : () => ({
		type: 'error',
		text: 'Memo field not long enough',
	})),
	validator ('memo', 'Memo', memo => memo.length < 24 ? null : () => ({
		type: 'warning',
		text: 'Memo field too long'
	})),
	validator ('externaliseline_set', 'Externalize set', set => set.reduce (( accumulator, current ) => accumulator && isMoney (current.amount.amount), true) ? null : () => ({
		type: 'error',
		text: 'Some money input is invalid.',
	})),
	validator ('externaliseline_set', 'Externalize set', set => set.reduce (( accumulator, current ) => accumulator && current.count > 0, true) ? null : () => ({
		type: 'error',
		text: 'Some product count is invalid.',
	})),
	validator ('externaliseline_set', 'Externalize set', set => set.reduce (( accumulator, current ) => accumulator && current.article, true) ? null : () => ({
		type: 'error',
		text: 'Some product is not set.',
	})),
];

export function* externalizeValidator () {
	const current = yield select (getExternalisationActiveObject);
	const res = validate (current, validations);
	yield put (actions.setValidations (res));
}

export default function* saga () {
	yield takeEvery (actions.SET_FIELD_ACTION, externalizeValidator);
	yield takeEvery (actions.CREATE_ACTION, externalizeValidator);

	yield takeLatest (actions.FETCH_ALL_ACTION, fetchAll);
	yield takeEvery (actions.CREATE_ACTION, create);
	yield takeLatest (actions.CREATE_SUCCESS, createSuccess);
}
