/* eslint-disable no-undef */

import { login } from './saga.js';
import fetch from 'isomorphic-fetch';
import { put } from 'redux-saga/effects';

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

	expect(l).toMatchObject({
		value: {
			CALL: {
				args: [
					'mock_url/auth/login/',
					{
						method: 'POST',
						body: {},
					},
				],
				fn: fetch,
			},
		},
		done: false,
	});

	for (const k in l.value.CALL.args) {
		if (typeof l.value.CALL.args[k] === 'object') {
			const data = l.value.CALL.args[k].body;

			expect(data.get('username')).toBe('testuser');
			expect(data.get('password')).toBe('testpassword');
		}
	}

	// Test the deserialization call of the request
	const mockfun = jest.fn();

	mockfun.mockReturnValue('asdfghjkl;');
	l = generator.next({
		ok: true,
		json: mockfun,
	});
	expect(mockfun.mock.calls.length).toBe(1);
	expect(l.value).toBe('asdfghjkl;');

	l = generator.next({
		token: '123456789',
		user: '%user%',
	});

	console.log(JSON.stringify(l));
	expect(l).toMatchObject({
		value: {
			'@@redux-saga/IO': true,
			'CALL': {
				context: null,
				args: [
					{
						type: 'AUTH_LOGIN_SUCCESS',
						data: {
							token: '123456789',
							user: '%user%',
						},
					},
				],
				fn: put,
			},
		},
		done: false,
	});

	// TODO: Handle reroute;
});
