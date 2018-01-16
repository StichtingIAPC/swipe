/* eslint-disable no-undef */

import { nextStep, isObject, done, isValue, notDone, formOf, exportsSagas } from '../../tools/sagaTestHelpers';

import { login, logout, loginRestore, saveLoginDetails, saveLogoutDetails, redirectLogin, saga } from './saga.js';
import fetch from 'isomorphic-fetch';
import { push } from 'react-router-redux';
import { call, put, select, takeEvery, takeLatest } from 'redux-saga/effects';
import { loginError, loginSuccess, logoutError, logoutSuccess, setRouteAfterAuthentication } from './actions';
import { __unsafeGetToken } from '../../api';
import config from '../../config';

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
		const generator = login({
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

		// Test the loginSuccess state update
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
				'CALL': {
					context: null,
					fn: select,
				},
			}),
		]);

		expect(result.value.CALL.args[0]({ auth: { nextRoute: '/nextRouteasdf/' }})).toBe('/nextRouteasdf/');

		// Test the redirect
		nextStep(generator, [
			notDone,
			isObject(put(push('/placeholderpath/'))),
		], '/placeholderpath/');

		// Test the authentication route change
		nextStep(generator, [
			done,
			isObject(put(setRouteAfterAuthentication('/'))),
		]);
	});

	test('failing due to backend denying', () => {
		const generator = login({
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
			isObject(put.resolve(loginError(null))),
		], {});

		nextStep(generator, [
			notDone,
			isObject({
				'@@redux-saga/IO': true,
				'CALL': {
					context: null,
					fn: select,
				},
			}),
		]);

		nextStep(generator, [
			done,
			isObject(put(loginError('Failed to connect'))),
		], 'Failed to connect');
	});

	test('failing with null error', () => {
		const generator = login({
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
			isObject(put.resolve(loginError(null))),
		], {});

		const result = nextStep(generator, [
			notDone,
			isObject({
				'@@redux-saga/IO': true,
				'CALL': {
					context: null,
					fn: select,
				},
			}),
		]);

		expect(result.value.CALL.args[0]({ auth: { error: [ 'ASDF' ]}})).toBe('ASDF');

		nextStep(generator, [
			done,
			isObject(put(loginError('Server not connected, please try again later.'))),
		], null);
	});

	test('Missing next route', () => {
		const generator = login({
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

		// Test the loginSuccess state update
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
				'CALL': {
					context: null,
					fn: select,
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
		const generator = logout();

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
			done,
			isObject(put(push('/authentication/login'))),
		]);
	});

	test('failing due to backend denying', () => {
		const generator = logout();

		nextStep(generator, [
			notDone,
			isObject(call(fetch, `mock_url/auth/logout/`, {
				method: 'POST',
				body: formOf({ token: __unsafeGetToken() }),
			})),
		]);
		nextStep(generator, [
			done,
			isObject(put(logoutError({ ok: false }))),
		], { ok: false });
	});
});

describe('Login restore', () => {
	test('successful', () => {
		const generator = loginRestore({
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
			done,
			isObject(put(loginSuccess('1234abcd', { username: 'testuser' }))),
		], {
			valid: true,
			user: { username: 'testuser' },
		});
	});

	test('failing due to backend denying', () => {
		const generator = loginRestore({
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
			done,
			isObject(put(loginError({ ok: false }))),
		], {
			ok: false,
		});
	});

	test('failing due to incorrect data', () => {
		const generator = loginRestore({
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
			done,
			isObject(put(loginError({ valid: false }))),
		], {
			valid: false,
		});
	});

	test('failing due to removed local storage', () => {
		nextStep(loginRestore({}), [
			done,
			isObject(put(loginError('Login restore failed'))),
		]);
	});

	test('failing restore due to invalid restore data', () => {
		nextStep(loginRestore({ loginAction: {}}), [
			done,
			isObject(put(loginError('Login restore failed'))),
		]);
	});
});

describe('Login and logout action save', () => {
	test('Successfull', () => {
		saveLoginDetails({
			action: 'AUTH_LOGIN_SUCCESS',
			data: {
				token: 'qo3n5ch',
				user: {
					name: 'testuser1998',
				},
			},
		});

		expect(JSON.parse(window.localStorage.getItem('LAST_LOGIN_SUCCESS_ACTION'))).toMatchObject({
			action: 'AUTH_LOGIN_SUCCESS',
			data: {
				token: 'qo3n5ch',
				user: {
					name: 'testuser1998',
				},
			},
		});

		saveLogoutDetails();

		expect(window.localStorage.getItem('LAST_LOGIN_SUCCESS_ACTION')).toBe(null);
	});

	test('Missing localStorage', () => {
		delete window.localStorage;

		saveLoginDetails({
			action: 'AUTH_LOGIN_SUCCESS',
			data: {
				token: 'qo3n5ch',
				user: {
					name: 'testuser1998',
				},
			},
		});

		saveLogoutDetails();
	});
});

test('Redirect after login', () => {
	nextStep(redirectLogin(), [
		done,
		isObject(put(push('/authentication/login'))),
	]);
});

test('Exports all necessary sagas', () => {
	exportsSagas(saga(), {
		AUTH_START_LOGIN: {
			fun: login,
			type: takeEvery,
		},
		AUTH_LOGIN_SUCCESS: {
			fun: saveLoginDetails,
			type: takeEvery,
		},
		AUTH_LOGIN_ERROR: {
			fun: redirectLogin,
			type: takeEvery,
		},
		AUTH_LOGIN_RESTORE: {
			fun: loginRestore,
			type: takeEvery,
		},
		AUTH_START_LOGOUT: {
			fun: logout,
			type: takeEvery,
		},
		AUTH_LOGOUT_SUCCESS: {
			fun: saveLogoutDetails,
			type: takeEvery,
		},
	});
});
