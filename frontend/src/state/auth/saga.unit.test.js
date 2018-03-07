/* eslint-disable no-undef */

import { nextStep, isObject, done, isValue, notDone, formOf, exportsSagas } from '../../tools/sagaTestHelpers';

import { onLogin, onLogout, onLoginRestore, onLoginSuccess, onLogoutSuccess, onLoginError, saga } from './saga.js';
import fetch from 'isomorphic-fetch';
import { push } from 'react-router-redux';
import { call, put, select, takeEvery, takeLatest } from 'redux-saga/effects';
import {
	loginError, loginSuccess, logoutError, logoutSuccess, setAuthToken,
	setRouteAfterAuthentication
} from './actions';
import { __unsafeGetToken, setToken } from '../../api';
import config from '../../config';
import { onLogoutError, onSetAuthToken } from './saga';

jest.mock('../../config.js', () => ({
	backendUrl: 'mock_url',
}));


beforeEach(() => {
	const localStorageMock = (() => {
		let store = {};

		return {
			getItem: key => store[key] || null,
			setItem: (key, value) => {
				store[key] = value.toString();
			},
			removeItem: key => {
				delete store[key];
			},
			clear: () => {
				store = {};
			},
		};
	})();

	Object.defineProperty(window, 'localStorage', {
		value: localStorageMock,
		configurable: true,
	});
});

describe('Login', () => {
	test('successful', () => {
		const generator = onLogin({
			username: 'testuser',
			password: 'testpassword',
		});

		// Test the request
		nextStep(generator, [
			notDone,
			isObject(call(fetch, `mock_url/auth/login/`, {
				method: 'POST',
				body: formOf({
					username: 'testuser',
					password: 'testpassword',
				}),
			})),
		]);

		// Test the deserialization call of the request
		const mockfun = jest.fn().mockReturnValue('asdfghjkl;');

		nextStep(generator, [
			notDone,
			isValue('asdfghjkl;'),
		], {
			ok: true,
			json: mockfun,
		});
		expect(mockfun.mock.calls.length).toBe(1);

		// Test the onLoginSuccess state update
		nextStep(generator, [
			notDone,
			isObject(put(loginSuccess('123456789', {
				name: 'username',
				permissions: [],
			}))),
		], {
			token: '123456789',
			user: {
				name: 'username',
				permissions: [],
			},
		});

		// This one cannot be tested simply using a repeat test.
		// This is because functions don't compare properly.
		// noinspection JSCheckFunctionSignatures
		const result = nextStep(generator, [
			notDone,
			isObject({
				'@@redux-saga/IO': true,
				'SELECT': {
					args: [],
				},
			}),
		]);

		expect(result.value.SELECT.selector({ auth: { nextRoute: '/nextRouteasdf/' }})).toBe('/nextRouteasdf/');

		// Test the redirect
		nextStep(generator, [
			notDone,
			isObject(put(push('/placeholderpath/'))),
		], '/placeholderpath/');

		// Test the authentication route change
		nextStep(generator, [
			notDone,
			isObject(put(setRouteAfterAuthentication('/'))),
		]);

		nextStep(generator, [ done, isValue() ]);
	});

	test('failing due to backend denying', () => {
		const generator = onLogin({
			username: 'testuser',
			password: 'testpassword',
		});

		// Test the request
		nextStep(generator, [
			notDone,
			isObject(call(fetch, `mock_url/auth/login/`, {
				method: 'POST',
				body: formOf({
					username: 'testuser',
					password: 'testpassword',
				}),
			})),
		]);

		// Test the deserialization call of the request
		const mockfun = jest.fn().mockReturnValue('asdfghjkl;');

		nextStep(generator, [
			notDone,
			isValue('asdfghjkl;'),
		], {
			ok: false,
			json: mockfun,
		});
		expect(mockfun.mock.calls.length).toBe(1);

		nextStep(generator, [
			notDone,
			isObject(put(loginError(null))),
		], {});

		nextStep(generator, [
			notDone,
			isObject({
				'@@redux-saga/IO': true,
				'SELECT': {
					args: [],
				},
			}),
		]);

		nextStep(generator, [
			notDone,
			isObject(put(loginError('Failed to connect'))),
		], 'Failed to connect');

		nextStep(generator, [ done, isValue() ]);
	});

	test('failing with null error', () => {
		const generator = onLogin({
			username: 'testuser',
			password: 'testpassword',
		});

		// Test the request
		nextStep(generator, [
			notDone,
			isObject(call(fetch, `mock_url/auth/login/`, {
				method: 'POST',
				body: formOf({
					username: 'testuser',
					password: 'testpassword',
				}),
			})),
		]);

		// Test the deserialization call of the request
		const mockfun = jest.fn().mockReturnValue('asdfghjkl;');

		nextStep(generator, [
			notDone,
			isValue('asdfghjkl;'),
		], {
			ok: false,
			json: mockfun,
		});
		expect(mockfun.mock.calls.length).toBe(1);

		nextStep(generator, [
			notDone,
			isObject(put(loginError(null))),
		], {});

		const result = nextStep(generator, [
			notDone,
			isObject({
				'@@redux-saga/IO': true,
				'SELECT': {
					args: [],
				},
			}),
		]);

		expect(result.value.SELECT.selector({ auth: { error: [ 'ASDF' ]}})).toBe('ASDF');

		nextStep(generator, [
			notDone,
			isObject(put(loginError('Server not connected, please try again later.'))),
		], null);

		nextStep(generator, [ done, isValue() ]);
	});

	test('Missing next route', () => {
		const generator = onLogin({
			username: 'testuser',
			password: 'testpassword',
		});

		// Test the request
		nextStep(generator, [
			notDone,
			isObject(call(fetch, `mock_url/auth/login/`, {
				method: 'POST',
				body: formOf({
					username: 'testuser',
					password: 'testpassword',
				}),
			})),
		]);

		// Test the deserialization call of the request
		const mockfun = jest.fn().mockReturnValue('asdfghjkl;');

		nextStep(generator, [
			notDone,
			isValue('asdfghjkl;'),
		], {
			ok: true,
			json: mockfun,
		});
		expect(mockfun.mock.calls.length).toBe(1);

		// Test the onLoginSuccess state update
		nextStep(generator, [
			notDone,
			isObject(put(loginSuccess('123456789', {
				name: 'username',
				permissions: [],
			}))),
		], {
			token: '123456789',
			user: {
				name: 'username',
				permissions: [],
			},
		});

		// This one cannot be tested simply using a repeat test.
		// This is because functions don't compare properly.
		nextStep(generator, [
			notDone,
			isObject({
				'@@redux-saga/IO': true,
				'SELECT': {
					args: [],
				},
			}),
		]);

		// Test the redirect
		nextStep(generator, [
			done,
		], null);
	});
});

describe('Logout', () => {
	test('successful', () => {
		const generator = onLogout();

		nextStep(generator, [
			notDone,
			isObject(call(fetch, `mock_url/auth/logout/`, {
				method: 'POST',
				body: formOf({ token: __unsafeGetToken() }),
			})),
		]);

		nextStep(generator, [
			notDone,
			isObject(put(logoutSuccess())),
		], { ok: true });

		nextStep(generator, [
			notDone,
			isObject(put(push('/authentication/login'))),
		]);

		nextStep(generator, [ done, isValue() ]);
	});

	test('failing due to backend denying', () => {
		const generator = onLogout();

		nextStep(generator, [
			notDone,
			isObject(call(fetch, `mock_url/auth/logout/`, {
				method: 'POST',
				body: formOf({ token: __unsafeGetToken() }),
			})),
		]);

		nextStep(generator, [
			notDone,
			isObject(put(logoutError({ ok: false }))),
		], { ok: false });

		nextStep(generator, [ done, isValue() ]);
	});
});

describe('Login restore', () => {
	test('successful', () => {
		const generator = onLoginRestore({
			loginAction: {
				data: {
					token: '1234abcd',
					user: {
						username: 'testuser',
					},
				},
			},
		});

		nextStep(generator, [
			notDone,
			isObject(call(fetch, `mock_url/auth/validate/`, {
				method: 'POST',
				body: formOf({
					token: '1234abcd',
					username: 'testuser',
				}),
			})),
		]);

		const mockfun = jest.fn().mockReturnValue('asdfghjkl;');

		nextStep(generator, [
			notDone,
			isValue('asdfghjkl;'),
		], {
			ok: true,
			json: mockfun,
		});
		expect(mockfun.mock.calls.length).toBe(1);

		nextStep(generator, [
			notDone,
			isObject(put(loginSuccess('1234abcd', { username: 'testuser' }))),
		], {
			valid: true,
			user: { username: 'testuser' },
		});

		nextStep(generator, [ done, isValue() ]);
	});

	test('failing due to backend denying', () => {
		const generator = onLoginRestore({
			loginAction: {
				data: {
					token: '4321bcda',
					user: {
						username: 'usertest',
					},
				},
			},
		});

		nextStep(generator, [
			notDone,
			isObject(call(fetch, `${config.backendUrl}/auth/validate/`, {
				method: 'POST',
				body: formOf({
					token: '4321bcda',
					username: 'usertest',
				}),
			})),
		]);

		nextStep(generator, [
			notDone,
			isObject(put(loginError({ ok: false }))),
		], {
			ok: false,
		});

		nextStep(generator, [ done, isValue() ]);
	});

	test('failing due to incorrect data', () => {
		const generator = onLoginRestore({
			loginAction: {
				data: {
					token: '4321bcda',
					user: {
						username: 'usertest',
					},
				},
			},
		});

		nextStep(generator, [
			notDone,
			isObject(call(fetch, `${config.backendUrl}/auth/validate/`, {
				method: 'POST',
				body: formOf({
					token: '4321bcda',
					username: 'usertest',
				}),
			})),
		]);

		const mockfun = jest.fn().mockReturnValue(';lkjhgfdsa');

		nextStep(generator, [
			notDone,
			isValue(';lkjhgfdsa'),
		], {
			ok: true,
			json: mockfun,
		});
		expect(mockfun.mock.calls.length).toBe(1);

		nextStep(generator, [
			notDone,
			isObject(put(loginError({ valid: false }))),
		], {
			valid: false,
		});

		nextStep(generator, [ done, isValue() ]);
	});

	test('failing due to removed local storage', () => {
		const generator = onLoginRestore({});

		nextStep(generator, [
			notDone,
			isObject(put(loginError('Login restore failed'))),
		]);

		nextStep(generator, [ done, isValue() ]);
	});

	test('failing restore due to invalid restore data', () => {
		const generator = onLoginRestore({ loginAction: {}});

		nextStep(generator, [
			notDone,
			isObject(put(loginError('Login restore failed'))),
		]);

		nextStep(generator, [ done, isValue() ]);
	});
});

describe('Logout success', () => {
	test('Successful', () => {
		window.localStorage.setItem('LAST_LOGIN_SUCCESS_ACTION', JSON.stringify({
			action: 'AUTH_LOGIN_SUCCESS',
			data: {
				token: 'qo3n5ch',
				user: {
					name: 'testuser1998',
				},
			},
		}));
		const generator = onLogoutSuccess();

		nextStep(generator, [
			notDone,
			isObject(put(setAuthToken(null))),
		]);

		expect(window.localStorage.getItem('LAST_LOGIN_SUCCESS_ACTION')).toBe(null);

		nextStep(generator, [ done, isValue() ]);
	});

	test('With missing localStorage', () => {
		delete window.localStorage;
		const generator = onLogoutSuccess();

		nextStep(generator, [
			notDone,
			isObject(put(setAuthToken(null))),
		]);

		nextStep(generator, [ done, isValue() ]);
	});
});

describe('Login success', () => {
	test('Successfull', () => {
		const generator = onLoginSuccess({
			action: 'AUTH_LOGIN_SUCCESS',
			data: {
				token: 'qo3n5ch',
				user: {
					name: 'testuser1998',
				},
			},
		});

		nextStep(generator, [
			notDone,
			isObject(put(setAuthToken('qo3n5ch'))),
		]);

		expect(JSON.parse(window.localStorage.getItem('LAST_LOGIN_SUCCESS_ACTION'))).toMatchObject({
			action: 'AUTH_LOGIN_SUCCESS',
			data: {
				token: 'qo3n5ch',
				user: {
					name: 'testuser1998',
				},
			},
		});

		nextStep(generator, [ done, isValue() ]);
	});

	test('Missing localStorage', () => {
		delete window.localStorage;

		onLoginSuccess({
			action: 'AUTH_LOGIN_SUCCESS',
			data: {
				token: 'qo3n5ch',
				user: {
					name: 'testuser1998',
				},
			},
		});
	});
});

test('Redirect after login', () => {
	const generator = onLoginError();

	nextStep(generator, [
		notDone,
		isObject(put(setAuthToken(null))),
	]);

	nextStep(generator, [
		notDone,
		isObject(put(push('/authentication/login'))),
	]);

	nextStep(generator, [ done, isValue() ]);
});

describe('Set auth token', () => {
	test('to null', () => {
		setToken('abcd1234');
		onSetAuthToken({ token: null });
		expect(__unsafeGetToken()).toBe(null);
	});

	test('to value', () => {
		setToken('null');
		onSetAuthToken({ token: '1234abcd' });
		expect(__unsafeGetToken()).toBe('1234abcd');
	});
});

test('Logout error', () => {
	const generator = onLogoutError();

	nextStep(generator, [
		notDone,
		isObject(put(setAuthToken(null))),
	]);

	nextStep(generator, [ done, isValue() ]);
});

test('Exports all necessary sagas', () => {
	exportsSagas(saga(), {
		AUTH_START_LOGIN: {
			fun: onLogin,
			type: takeEvery,
		},
		AUTH_LOGIN_SUCCESS: {
			fun: onLoginSuccess,
			type: takeEvery,
		},
		AUTH_LOGIN_ERROR: {
			fun: onLoginError,
			type: takeEvery,
		},
		AUTH_LOGIN_RESTORE: {
			fun: onLoginRestore,
			type: takeEvery,
		},
		AUTH_START_LOGOUT: {
			fun: onLogout,
			type: takeEvery,
		},
		AUTH_LOGOUT_SUCCESS: {
			fun: onLogoutSuccess,
			type: takeEvery,
		},
		AUTH_LOGOUT_ERROR: {
			fun: onLogoutError,
			type: takeEvery,
		},
		AUTH_SET_TOKEN: {
			fun: onSetAuthToken,
			type: takeEvery,
		},
	});
});
