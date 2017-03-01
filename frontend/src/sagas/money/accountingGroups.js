import { call, put } from "redux-saga/effects";
import { push } from "react-router-redux";
import {
	startFetchingAccountingGroups,
	doneFetchingAccountingGroups,
	accountingGroupInputError,
	accountingGroupFetchError
} from "../../actions/money/accountingGroups";
import { get, post, put as api_put } from "../../api";

export function* fetchAccountingGroups({ redirectTo }) {
	try {
		const data = yield (yield call(
			get,
			'/money/accountinggroup/',
		)).json();
		yield put(doneFetchingAccountingGroups(data));
		if (redirectTo)
			yield put(push(redirectTo));
	} catch (e) {
		yield put(accountingGroupFetchError(e.message));
	}
}

export function* createAccountingGroup({ accGrp }) {
	const accountingGroup = {...accGrp};
	try {
		const data = yield (yield call(
			post,
			'/money/accountinggroup/',
			accountingGroup,
		)).json();
		yield put(startFetchingAccountingGroups({
			redirectTo: `/money/accountinggroup/${data.iso}/`,
		}));
	} catch (e) {
		let msg;
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = yield call(e.json.bind(e));
		yield put(accountingGroupInputError(msg));
	}
}

export function* updateAccountingGroup({ accGrp }) {
	const accountingGroup = {...accGrp};
	try {
		const data = yield (yield call(
			api_put,
			`/money/accountinggroup/${accountingGroup.iso}/`,
			accountingGroup,
		)).json();
		yield put(startFetchingAccountingGroups({
			redirectTo: `/money/accountinggroup/${data.iso}/`,
		}));
	} catch (e) {
		let msg;
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = yield call(e.json.bind(e));
		yield put(accountingGroupInputError(msg));
	}
}
