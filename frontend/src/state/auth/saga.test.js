/* eslint-disable no-undef */

import { login } from './saga.js';
import fetch from 'isomorphic-fetch';
import { push } from 'react-router-redux';
import { call, put, select } from 'redux-saga/effects';
import { loginSuccess, setRouteAfterAuthentication } from './actions';

jest.mock('../../config.js', () => ({
	backendUrl: 'mock_url',
}));


test('A successful login', () => {
	const generator = login({
		username: 'testuser',
		password: 'testpassword',
	});

	// Test the request
	let l = generator.next();
	const form = new FormData();

	form.append('username', 'testuser');
	form.append('password', 'testpassword');
	expect(l.value).toMatchObject(call(fetch, `mock_url/auth/login/`, {
		method: 'POST',
		body: form,
	}));
	expect(l.done).toBe(false);

	// Test the deserialization call of the request
	const mockfun = jest.fn();

	mockfun.mockReturnValue('asdfghjkl;');
	l = generator.next({
		ok: true,
		json: mockfun,
	});
	expect(mockfun.mock.calls.length).toBe(1);
	expect(l.value).toBe('asdfghjkl;');
	expect(l.done).toBe(false);

	// Test the loginSuccess state update
	l = generator.next({
		token: '123456789',
		user: {
			name: 'username',
			permissions: [],
		},
	});
	expect(l.value).toMatchObject(call(put, loginSuccess('123456789', {
		name: 'username',
		permissions: [],
	})));
	expect(l.done).toBe(false);

	// This one cannot be tested simply using a repeat test.
	// This is because functions don't compare properly.
	l = generator.next();
	expect(l.value).toMatchObject({
		'@@redux-saga/IO': true,
		'SELECT': {
			args: [],
		},
	});
	expect(l.done).toBe(false);

	l = generator.next('/placeholderpath/');
	expect(l.value).toMatchObject(put(push('/placeholderpath/')));
	expect(l.done).toBe(false);

	l = generator.next();
	expect(l.value).toMatchObject(put(setRouteAfterAuthentication('/')));
	expect(l.done).toBe(true);
});
