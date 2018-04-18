import { call, put, takeEvery, takeLatest, select } from 'redux-saga/effects';
import { push } from 'react-router-redux';
import store from '../../store';

import * as api from './api';
import * as actions from './actions';
import { cleanErrorMessage } from '../../../tools/sagaHelpers';
import { getExternalisationActiveObject, getExternalisationLoading } from './selectors';
import { isMoney, validate, validator } from '../../../tools/validations/validators';

export function* fetchAll() {
	if (yield select(getExternalisationLoading)) {
		return;
	}
	yield put(actions.setLoadingAction());
	try {
		const externalizations = yield (yield call(api.getAll)).json();

		const exts = [].concat.apply([], externalizations.map(e => e.externaliseline_set.map(en => ({
			memo: e.memo,
			count: en.count,
			amount: en.cost,
			article: en.article_type,
		}))));

		yield put(actions.fetchAllExternalizesSuccess(exts));
	} catch (e) {
		console.error(e);
		yield put(actions.fetchAllExternalizesFail(e));
	} finally {
		yield put(actions.fetchAllExternalizesFinally());
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

		yield put(actions.createExternalizeSuccess(newExternalise));
	} catch (e) {
		yield put(actions.createExternalizeFail(cleanErrorMessage(e)));
	} finally {
		yield put(actions.createExternalizeFinally());
	}
}

export function* createSuccess() {
	yield put(actions.fetchAllExternalizesStart());
	yield put(push('/logistics/externalise'));
}

const validations = [
	validator('memo', 'Memo', memo => memo.length > 3 ? null : () => ({
		type: 'error',
		text: 'Memo field not long enough',
	})),
	validator('memo', 'Memo', memo => memo.length < 24 ? null : () => ({
		type: 'warning',
		text: 'Memo field too long',
	})),
	validator('externaliseline_set', 'Externalize set', set => set.reduce((accumulator, current) => accumulator && isMoney(current.amount.amount), true) ? null : () => ({
		type: 'error',
		text: 'Some money input is invalid.',
	})),
	validator('externaliseline_set', 'Externalize set', set => set.reduce((accumulator, current) => accumulator && current.count > 0, true) ? null : () => ({
		type: 'error',
		text: 'Some product count is invalid.',
	})),
	validator('externaliseline_set', 'Externalize set', set => set.reduce((accumulator, current) => accumulator && current.article, true) ? null : () => ({
		type: 'error',
		text: 'Some product is not set.',
	})),
];

export function* externalizeValidator() {
	const current = yield select(getExternalisationActiveObject);
	const res = validate(current, validations);

	yield put(actions.setValidations(res));
}

export default function* saga() {
	yield takeEvery(actions.LOGISTICS_EXTRNALIZE_SET_FIELD, externalizeValidator);
	yield takeEvery(actions.LOGISTICS_EXTRNALIZE_CREATE_START, externalizeValidator);

	yield takeLatest(actions.LOGISTICS_EXTRNALIZE_FETCH_ALL_START, fetchAll);
	yield takeEvery(actions.LOGISTICS_EXTRNALIZE_CREATE_START, create);
	yield takeLatest(actions.LOGISTICS_EXTRNALIZE_CREATE_SUCCESS, createSuccess);
}
