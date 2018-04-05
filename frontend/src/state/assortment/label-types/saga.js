import { call, put, takeEvery, takeLatest } from 'redux-saga/effects';
import { push } from 'react-router-redux';

import * as actions from './actions.js';
import { cleanErrorMessage } from '../../../tools/sagaHelpers';
import * as api from './api';

function* fetchAllLabelTypes({ redirectTo }) {
	try {
		const labelType = yield (yield call(api.getAll)).json();

		yield put(actions.fetchAllLabelTypesDone(labelType));
		if (redirectTo) {
			yield put(push(redirectTo));
		}
	} catch (e) {
		yield put(actions.fetchAllLabelTypesFailed(cleanErrorMessage(e)));
	} finally {
		yield put(actions.fetchAllLabelTypesFinally());
	}
}

function* fetchLabelType({ id }) {
	try {
		const newLabelType = yield (yield call(api.get, id)).json();

		yield put(actions.fetchLabelTypeDone(newLabelType));
	} catch (e) {
		yield put(actions.fetchLabelTypeFailed(id, e));
	} finally {
		yield put(actions.fetchLabelTypeFinally());
	}
}

function* createLabelType({ labelType }) {
	const document = { ...labelType };

	try {
		const newLabelType = yield (yield call(api.post, document)).json();

		yield put(actions.createLabelTypeDone(newLabelType));
		yield put(actions.fetchAllLabelTypes('/assortment/'));
	} catch (e) {
		yield put(actions.createLabelTypeFailed(cleanErrorMessage(e)));
	} finally {
		yield put(actions.createLabelTypeFinally());
	}
}

function* updateLabelType({ labelType }) {
	const document = { ...labelType };

	try {
		const newLabelType = yield (yield call(api.put, labelType.id, document)).json();

		yield put(actions.updateLabelTypeDone(newLabelType));
		yield put(actions.fetchAllLabelTypes('/assortment/'));
	} catch (e) {
		yield put(actions.updateLabelTypeFailed(cleanErrorMessage(e)));
	} finally {
		yield put(actions.updateLabelTypeFinally());
	}
}

function* deleteLabelType({ labelType }) {
	const document = { ...labelType };

	try {
		const newLabelType = yield (yield call(api.del, labelType.id, document)).json();

		yield put(actions.deleteLabelTypeDone(newLabelType));
		yield put(actions.fetchAllLabelTypes(`/assortment/`));
	} catch (e) {
		yield put(actions.deleteLabelTypeFailed(cleanErrorMessage(e)));
	} finally {
		yield put(actions.deleteLabelTypeFinally());
	}
}

export default function* saga() {
	yield takeLatest('assortment/label-types/FETCH_ALL', fetchAllLabelTypes);
	yield takeLatest('assortment/label-types/FETCH', fetchLabelType);
	yield takeEvery('assortment/label-types/CREATE', createLabelType);
	yield takeEvery('assortment/label-types/UPDATE', updateLabelType);
	yield takeEvery('assortment/label-types/DELETE', deleteLabelType);
}
