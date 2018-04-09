import { call, put, takeEvery, takeLatest } from 'redux-saga/effects';
import { push } from 'react-router-redux';
import * as api from './api';
import { doneFetchingRegisters, registerFetchError, registerInputError, startFetchingRegisters } from './actions';

function* fetchRegisters({ redirectTo } = {}) {
	let msg = null;

	try {
		const data = yield (yield call(api.getAll)).json();

		yield put(doneFetchingRegisters(data));
		if (redirectTo) {
			yield put(push(redirectTo));
		}
	}	catch (e) {
		if (e instanceof Error) {
			msg = e.message;
		}
		if (e instanceof Response) {
			msg = e.json();
		}

		yield put(registerFetchError(msg));
	}
}

function* createRegister({ register } = {}) {
	const document = { ...register };
	let msg = null;

	try {
		const data = yield (yield call(api.post, document)).json();

		yield put(startFetchingRegisters({ redirectTo: `/register/register/${data.id}/` }));
	} catch (e) {
		if (e instanceof Error) {
			msg = e.message;
		}
		if (e instanceof Response) {
			msg = e.json();
		}

		yield put(registerInputError(msg));
	}
}

function* updateRegister({ register } = {}) {
	const document = { ...register };
	let msg = null;

	try {
		const data = yield (yield call(api.put, register.id, document)).json();

		yield put(startFetchingRegisters({ redirectTo: `/register/register/${data.id}/` }));
	} catch (e) {
		if (e instanceof Error) {
			msg = e.message;
		}
		if (e instanceof Response) {
			msg = e.json();
		}

		yield put(registerInputError(msg));
	}
}

export default function* saga() {
	yield takeLatest('REGISTER_FETCH_START', fetchRegisters);
	yield takeEvery('REGISTER_CREATE', createRegister);
	yield takeEvery('REGISTER_UPDATE', updateRegister);
	yield takeEvery('REGISTER_DELETE', updateRegister);
}
