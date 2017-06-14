import { call, put } from 'redux-saga/effects';
import { push } from 'react-router-redux';
import { get, post, put as api_put } from '../../api';
import {
	doneFetchingRegisters,
	registerFetchError,
	registerInputError,
	startFetchingRegisters
} from '../../actions/register/registers';

export function* fetchRegisters({ redirectTo } = {}) {
	let msg = null;

	try {
		const data = yield (yield call(
			get,
			'/register/',
		)).json();

		yield put(doneFetchingRegisters(data));
		if (redirectTo)
			yield put(push(redirectTo));
	}	catch (e) {
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = e.json();

		yield put(registerFetchError(msg));
	}
}

export function* createRegister({ register } = {}) {
	const document = { ...register };
	let msg = null;

	try {
		const data = yield (yield call(
			post,
			'/register/',
			document,
		)).json();

		yield put(startFetchingRegisters({ redirectTo: `/register/register/${data.id}/` }));
	} catch (e) {
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = e.json();

		yield put(registerInputError(msg));
	}
}

export function* updateRegister({ register } = {}) {
	const document = { ...register };
	let msg = null;

	try {
		const data = yield (yield call(
			api_put,
			`/register/${register.id}/`,
			document,
		)).json();

		yield put(startFetchingRegisters({ redirectTo: `/register/register/${data.id}/` }));
	} catch (e) {
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = e.json();

		yield put(registerInputError(msg));
	}
}
