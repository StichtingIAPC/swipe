import { call, put, select, takeEvery } from 'redux-saga/effects';
import { push } from 'react-router-redux';
import { loginError, loginSuccess, setRouteAfterAuthentication } from './actions.js';
import config from '../../config.js';
import fetch from 'isomorphic-fetch';
import { __unsafeGetToken } from '../../api';
import { logoutError, logoutSuccess } from './actions';

export function* login({ username, password }) {
	const form = new FormData();

form.append('username', username);
	form.append('password', password);
	try {
		const result = yield call(fetch, `${config.backendUrl}/auth/login/`, {
			method: 'POST',
			body: form,
		});

		if (!result.ok) {
			throw yield result.json();
		}


		const data = yield result.json();

		yield call(put, loginSuccess(data.token, data.user));

		const nextRoute = yield select(state => state.auth.nextRoute);

		if (nextRoute !== null) {
			yield put(push(nextRoute));
			return put(setRouteAfterAuthentication('/'));
		}
	} catch (e) {
		yield put.resolve(loginError(e.non_field_errors || null));
		let err = yield select(state => state.auth.error && state.auth.error[0]);

		// eslint-disable-next-line
		if (err === null || err === undefined) {
			err = 'Server not connected, please try again later.';
		}
		return put(loginError(err));
	}
}

export function* logout() {
	const token = __unsafeGetToken();

	const form = new FormData();

	form.append('token', token);
	try {
		const result = yield call(fetch, `${config.backendUrl}/auth/logout/`, {
			method: 'POST',
			body: form,
		});

		if (!result.ok) {
			throw result;
		}

		yield put(logoutSuccess());
		return put(push('/authentication/login'));
	} catch (e) {
		return put(logoutError(e));
	}
}

export function* loginRestore({ loginAction }) {
	if (!loginAction) {
		return put(loginError('Login restore failed'));
	}
	const action = loginAction.data;

	if (!(action && action.token && action.user && action.user.username)) {
		return put(loginError('Login restore failed'));
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
			throw result;
		}

		const data = yield result.json();

		if (!data.valid) {
			throw data;
		}

		return put(loginSuccess(token, data.user));
	} catch (e) {
		return put(loginError(e));
	}
}

export function saveLoginDetails(action) {
	if (!window || !window.localStorage) {
		return;
	}

	window.localStorage.setItem('LAST_LOGIN_SUCCESS_ACTION', JSON.stringify(action));
}

export function saveLogoutDetails() {
	if (!window || !window.localStorage) {
		return;
	}

	window.localStorage.removeItem('LAST_LOGIN_SUCCESS_ACTION');
}

export function* redirectLogin() {
	yield put(push('/authentication/login'));
}

export function* saga() {
	yield takeEvery('AUTH_START_LOGIN', login);
	yield takeEvery('AUTH_LOGIN_SUCCESS', saveLoginDetails);
	yield takeEvery('AUTH_LOGIN_ERROR', redirectLogin);
	yield takeEvery('AUTH_LOGIN_RESTORE', loginRestore);
	yield takeEvery('AUTH_START_LOGOUT', logout);
	yield takeEvery('AUTH_LOGOUT_SUCCESS', saveLogoutDetails);
}
