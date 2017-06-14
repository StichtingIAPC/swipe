import { call, put } from 'redux-saga/effects';
import { push } from 'react-router-redux';
import { get } from '../../api';
import {
	doneFetchingOpenRegisterCounts,
	openRegisterCountFetchError
} from '../../actions/register/registerCount/openRegisters';
import {
	closedRegisterCountFetchError,
	doneFetchingClosedRegisterCounts
} from '../../actions/register/registerCount/closedRegisters';

export function* fetchOpenRegisterCounts({ redirectTo }) {
	try {
		const data = yield (yield call(
			get,
			'/register/opened/',
		)).json();

		yield put(doneFetchingOpenRegisterCounts(data));
		if (redirectTo)
			yield put(push(redirectTo));
	}	catch (e) {
		yield put(openRegisterCountFetchError(e.message));
	}
}

export function* fetchClosedRegisterCounts({ redirectTo }) {
	try {
		const data = yield (yield call(
			get,
			'/register/closed/',
		)).json();

		yield put(doneFetchingClosedRegisterCounts(data));
		if (redirectTo)
			yield put(push(redirectTo));
	}	catch (e) {
		yield put(closedRegisterCountFetchError(e.message));
	}
}
