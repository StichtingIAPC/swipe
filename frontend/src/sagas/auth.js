import { call, put, select } from 'redux-saga/effects';
import { push } from 'react-router-redux';
import { loginError, loginSuccess, setRouteAfterAuthentication } from '../actions/auth.js';
import config from '../config.js';
import fetch from 'isomorphic-fetch';
import { getToken } from '../api';
import { logoutError, logoutSuccess } from '../actions/auth';

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

		yield put(loginSuccess(data.token, data.user));

		const nextRoute = yield select(state => state.auth.nextRoute);

		if (nextRoute !== null) {
			yield put(push(nextRoute));
			yield put(setRouteAfterAuthentication('/'));
		}
	} catch (e) {
		yield put(loginError(e));
	}
}

export function saveLogoutDetails() {
	if (!window || !window.localStorage) {
		return;
	}
	window.localStorage.removeItem('LAST_LOGIN_SUCCESS_ACTION');
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

export function saveLoginDetails(action) {
	if (!window || !window.localStorage) {
		return;
	}
	window.localStorage.setItem('LAST_LOGIN_SUCCESS_ACTION', JSON.stringify(action));
}

