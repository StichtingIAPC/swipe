import { call, put, select, takeEvery } from 'redux-saga/effects';
import { push } from 'react-router-redux';
import { loginError, loginSuccess, setRouteAfterAuthentication } from './actions.js';
import config from '../../config.js';
import fetch from 'isomorphic-fetch';
import { getToken } from '../../api';
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
			yield put(setRouteAfterAuthentication('/'));
		}
	} catch (e) {
		yield put(loginError(e));
	}
}

export function* logout() {
	const token = yield getToken();

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
		yield put(push('/authentication/login'));
	} catch (e) {
		yield put(logoutError(e));
	}
}

export function* loginRestore({ loginAction }) {
	const { data: { token, user: { username } } } = loginAction;

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

		yield put(loginSuccess(token, data.user));
	} catch (e) {
		yield put(loginError(e));
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
