import { call, put, takeEvery, takeLatest } from 'redux-saga/effects';
import { push } from 'react-router-redux';

import * as actions from './actions.js';
import * as api from '../../../api';
import { cleanErrorMessage } from '../../../tools/sagaHelpers';

function* fetchAllAccountingGroups({redirectTo}) {
	try {
		const accountingGroups = yield (yield call(
			api.get,
			'/money/accountinggroup/',
		)).json();

		yield put(actions.fetchAllAccountingGroupsDone(accountingGroups));
		if (redirectTo) {
			yield put(push(redirectTo));
		}
	} catch (e) {
		yield put(actions.fetchAllAccountingGroupsFailed(cleanErrorMessage(e)));
	} finally {
		yield put(actions.fetchAllAccountingGroupsFinally());
	}
}

function* fetchAccountingGroup({id}) {
	try {
		const newAccountingGroup = yield (yield call(
			api.get,
			`/money/accountinggroup/${id}`,
		)).json();

		yield put(actions.fetchAccountingGroupDone(newAccountingGroup));
	} catch (e) {
		yield put(actions.fetchAccountingGroupFailed(id, cleanErrorMessage(e)));
	} finally {
		yield put(actions.fetchAccountingGroupFinally());
	}
}

function* createAccountingGroup({accountingGroup}) {
	const document = {...accountingGroup};

	try {
		const newAccountingGroup = yield (yield call(
			api.post,
			'/money/accountinggroup/',
			document,
		)).json();

		yield put(actions.createAccountingGroupDone(newAccountingGroup));
		yield put(actions.fetchAllAccountingGroups(`/__FILL_IN__/${newAccountingGroup.id}/`));
	} catch (e) {
		yield put(actions.createAccountingGroupFailed(accountingGroup, cleanErrorMessage(e)));
	} finally {
		yield put(actions.createAccountingGroupFinally());
	}
}

function* updateAccountingGroup({accountingGroup}) {
	const document = {...accountingGroup};

	try {
		const newAccountingGroup = yield (yield call(
			api.put,
			`/money/accountinggroup/${accountingGroup.id}/`,
			document,
		)).json();

		yield put(actions.updateAccountingGroupDone(newAccountingGroup));
		yield put(actions.fetchAllAccountingGroups(`/__FILL_IN__/${newAccountingGroup.id}/`));
	} catch (e) {
		yield put(actions.updateAccountingGroupFailed(accountingGroup, cleanErrorMessage(e)));
	} finally {
		yield put(actions.updateAccountingGroupFinally());
	}
}

function* deleteAccountingGroup({accountingGroup}) {
	const document = {...accountingGroup};

	try {
		const newAccountingGroup = yield (yield call(
			api.del,
			`/money/accountinggroup/${accountingGroup.id}/`,
			document,
		)).json();

		yield put(actions.deleteAccountingGroupDone(newAccountingGroup));
		yield put(actions.fetchAllAccountingGroups(`/__FILL_IN__/${newAccountingGroup.id}/`));
	} catch (e) {
		yield put(actions.deleteAccountingGroupFailed(accountingGroup, cleanErrorMessage(e)));
	} finally {
		yield put(actions.deleteAccountingGroupFinally());
	}
}

export default function* saga() {
	yield takeLatest('money/accounting-groups/FETCH_ALL', fetchAllAccountingGroups);
	yield takeLatest('money/accounting-groups/FETCH', fetchAccountingGroup);
	yield takeEvery('money/accounting-groups/CREATE', createAccountingGroup);
	yield takeEvery('money/accounting-groups/UPDATE', updateAccountingGroup);
	yield takeEvery('money/accounting-groups/DELETE', deleteAccountingGroup);
}
