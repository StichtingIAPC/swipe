import { call, put, takeEvery, takeLatest } from 'redux-saga/effects';
import { push } from 'react-router-redux';
import {
	accountingGroupFetchError,
	accountingGroupInputError,
	doneFetchingAccountingGroups,
	startFetchingAccountingGroups,
} from './actions';
import { get, post, put as api_put } from '../../../api.js';

function* fetchAccountingGroups({ redirectTo }) {
	let msg = null;

	try {
		const data = yield (yield call(
			get,
			'/money/accountinggroup/',
		)).json();

		yield put(doneFetchingAccountingGroups(data));
		if (redirectTo)
			yield put(push(redirectTo));
	} catch (e) {
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = yield e.json();

		yield put(accountingGroupFetchError(msg));
	}
}

function* createAccountingGroup({ accGrp }) {
	const accountingGroup = { ...accGrp };
	let msg = null;

	try {
		const data = yield (yield call(
			post,
			'/money/accountinggroup/',
			accountingGroup,
		)).json();

		yield put(startFetchingAccountingGroups({ redirectTo: `/money/accountinggroup/${data.id}/` }));
	} catch (e) {
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = yield e.json();

		yield put(accountingGroupInputError(msg));
	}
}

function* updateAccountingGroup({ accGrp }) {
	const accountingGroup = { ...accGrp };
	let msg = null;

	try {
		const data = yield (yield call(
			api_put,
			`/money/accountinggroup/${accountingGroup.id}/`,
			accountingGroup,
		)).json();

		yield put(startFetchingAccountingGroups({ redirectTo: `/money/accountinggroup/${data.id}/` }));
	} catch (e) {
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = yield e.json();

		yield put(accountingGroupInputError(msg));
	}
}

export default function* saga() {
	yield takeLatest('ACCOUNTING_GROUP_FETCH_START', fetchAccountingGroups);
	yield takeEvery('ACCOUNTING_GROUP_CREATE', createAccountingGroup);
	yield takeEvery('ACCOUNTING_GROUP_UPDATE', updateAccountingGroup);
}
