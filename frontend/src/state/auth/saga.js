import { call, put, select, takeEvery } from 'redux-saga/effects';
import { push } from 'react-router-redux';
import config from '../../config.js';
import fetch from 'isomorphic-fetch';
import { __unsafeGetToken, setToken } from '../../api';
import {
	logoutError,
	logoutSuccess,
	setAuthToken,
	loginError,
	loginSuccess,
	setRouteAfterAuthentication
} from './actions';

export function* onLogin({ username, password }) {
	const form = new FormData();

	form.append('username', username);
	form.append('password', password);
	try {
		const result = yield call(fetch, `${config.backendUrl}/auth/login/`, {
			method: 'POST',
			body: form,
		});

		if (!result.ok) {
			if (result.status === 401) {
				const text = yield result.text();

				if (text) {
					yield put(loginError(text));
				} else {
					yield put(loginError('Unable to log in'));
				}
			} else {
				yield put(loginError(`Backend responded with error code ${result.status.toString()}`));
			}
			return;
		}

		const data = yield result.json();

		yield put(loginSuccess(data.token, data.user));

		// noinspection JSCheckFunctionSignatures
		const nextRoute = yield select(state => state.auth.nextRoute);

		if (nextRoute !== null) {
			yield put(push(nextRoute));
			yield put(setRouteAfterAuthentication('/'));
		}
	} catch (e) {
		if (e.message === 'Failed to fetch') {
			yield put(loginError('Unable to connect to server'));
		} else {
			yield put(loginError(e));
		}
	}
}

export function* onLogout() {
	const token = __unsafeGetToken();

	const form = new FormData();

	form.append('token', token);
	try {
		const result = yield call(fetch, `${config.backendUrl}/auth/logout/`, {
			method: 'POST',
			body: form,
		});

		if (!result.ok) {
			throw `Backend responded with error code ${result.status.toString()}`;
		}

		yield put(logoutSuccess());
		yield put(push('/authentication/login'));
	} catch (e) {
		yield put(logoutError(e));
	}
}

export function* onLoginRestore({ loginAction }) {
	if (!loginAction) {
		yield put(loginError('Login restore failed'));
		// noinspection JSValidateTypes
		return;
	}
	const action = loginAction.data;

	if (!(action && action.token && action.user && action.user.username)) {
		yield put(loginError('Login restore failed'));
		// noinspection JSValidateTypes
		return;
	}

	const { token, user: { username }} = action;

	const form = new FormData();

	form.append('token', token);
	form.append('username', username);

	try {
		const result = yield call(fetch, `${config.backendUrl}/auth/validate/`, {
			method: 'POST',
			body: form,
		});

		if (!result.ok) {
			throw `Backend responded with error code ${result.status.toString()}`;
		}

		const data = yield result.json();

		if (!data.valid) {
			if (data.expiry) {
				throw 'Login expired because of inactivity';
			} else {
				throw '';
			}
		}

		yield put(loginSuccess(token, data.user));
	} catch (e) {
		yield put(loginError(e));
	}
}

export function* onLoginSuccess(action) {
	if (window && window.localStorage) {
		window.localStorage.setItem('LAST_LOGIN_SUCCESS_ACTION', JSON.stringify(action));
	}
	yield put(setAuthToken(action.data.token));
}

export function* onLogoutSuccess() {
	if (window && window.localStorage) {
		window.localStorage.removeItem('LAST_LOGIN_SUCCESS_ACTION');
	}
	yield put(setAuthToken(null));
}

export function* onLoginError() {
	yield put(setAuthToken(null));
	yield put(push('/authentication/login'));
}

export function* onLogoutError() {
	yield put(setAuthToken(null));
}

export function onSetAuthToken(action) {
	setToken(action.token);
}

export function* saga() {
	yield takeEvery('AUTH_START_LOGIN', onLogin);
	yield takeEvery('AUTH_LOGIN_SUCCESS', onLoginSuccess);
	yield takeEvery('AUTH_LOGIN_ERROR', onLoginError);
	yield takeEvery('AUTH_LOGIN_RESTORE', onLoginRestore);
	yield takeEvery('AUTH_START_LOGOUT', onLogout);
	yield takeEvery('AUTH_LOGOUT_SUCCESS', onLogoutSuccess);
	yield takeEvery('AUTH_LOGOUT_ERROR', onLogoutError);
	yield takeEvery('AUTH_SET_TOKEN', onSetAuthToken);
}
