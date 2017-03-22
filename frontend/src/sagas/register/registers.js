import { call, put } from "redux-saga/effects";
import { push } from "react-router-redux";
import { get, post, put as api_put } from "../../api";
import {
	startFetchingRegisters,
	doneFetchingRegisters,
	registerFetchError,
	registerInputError
} from "../../actions/register/registers";

export function* fetchRegisters({ redirectTo } = {}) {
	try {
		const data = yield (yield call(
			get,
			'/register/',
		)).json();
		yield put(doneFetchingRegisters(data));
		if (redirectTo) {
			yield put(push(redirectTo));
		}
	}	catch (e) {
		yield put(registerFetchError(e.message));
	}
}

export function* createRegister({ register } = {}) {
	const document = { ...register };

	try {
		const data = yield (yield call(
			post,
			'/register/',
			document,
		)).json();

		yield put(startFetchingRegisters({
			redirectTo: `/register/register/${data.id}/`,
		}));
	} catch (e) {
		let msg;
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = e.json();
		yield put(registerInputError(msg));
	}
}

export function* updateRegister({ register } = {}) {
	const document = { ...register };

	try {
		const data = yield (yield call(
			api_put,
			`/register/${register.id}/`,
			document,
		)).json();

		yield put(startFetchingRegisters({
			redirectTo: `/register/register/${data.id}/`,
		}));
	} catch (e) {
		let msg;
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = e.json();
		yield put(registerInputError(msg));
	}
}
