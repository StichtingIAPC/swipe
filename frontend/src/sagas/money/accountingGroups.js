import { call, put } from 'redux-saga/effects';
import { push } from 'react-router-redux';
import {
	accountingGroupFetchError,
	accountingGroupInputError,
	doneFetchingAccountingGroups,
	startFetchingAccountingGroups
} from '../../actions/money/accountingGroups';
import { get, post, put as api_put } from '../../api';

export function* fetchAccountingGroups({ redirectTo }) {
	let msg = null;

	try {
		const data = yield (yield call(
			get,
			'/money/accountinggroup/',
		)).json();

		yield put(doneFetchingAccountingGroups(data));
		if (redirectTo) {
			yield put(push(redirectTo));
		}
	} catch (e) {
		if (e instanceof Error) {
			msg = e.message;
		}
		if (e instanceof Response) {
			msg = yield e.json();
		}

		yield put(accountingGroupFetchError(msg));
	}
}

export function* createAccountingGroup({ accGrp }) {
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
		if (e instanceof Error) {
			msg = e.message;
		}
		if (e instanceof Response) {
			msg = yield e.json();
		}

		yield put(accountingGroupInputError(msg));
	}
}

export function* updateAccountingGroup({ accGrp }) {
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
		if (e instanceof Error) {
			msg = e.message;
		}
		if (e instanceof Response) {
			msg = yield e.json();
		}

		yield put(accountingGroupInputError(msg));
	}
}
