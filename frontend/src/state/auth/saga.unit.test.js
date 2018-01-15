/* eslint-disable no-undef */

import { nextStep, isObject, done, isValue, notDone, formOf } from '../../tools/sagaTestHelpers';

import { login, logout, loginRestore } from './saga.js';
import fetch from 'isomorphic-fetch';
import { push } from 'react-router-redux';
import { call, put } from 'redux-saga/effects';
import { loginError, loginSuccess, logoutError, logoutSuccess, setRouteAfterAuthentication } from './actions';
import { __unsafeGetToken } from '../../api';

jest.mock('../../config.js', () => ({
	backendUrl: 'mock_url',
}));


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
			isObject(call(put, loginSuccess('123456789', {
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
				'SELECT': {
					args: [],
				},
			}),
		]);

		nextStep(generator, [
			done,
			isObject(put(loginError('Failed to connect'))),
		], 'Failed to connect');
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
