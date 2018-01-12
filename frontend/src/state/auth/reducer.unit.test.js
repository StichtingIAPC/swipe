/* eslint-disable no-undefined,no-undef */
import authenticationReducer from './reducer';

jest.mock('../../config.js', () => ({
	backendUrl: 'mock_url',
}));

describe('Authentication reducer state', () => {
	describe('SET_ROUTE_AFTER_AUTH', () => {
		test('without existing state', () => {
			expect(authenticationReducer(undefined, {
				type: 'AUTH_SET_ROUTE_AFTER_AUTH',
				route: '/arbitrary/test/route',
			})).toMatchObject({
				...authenticationReducer(undefined, {}),
				nextRoute: '/arbitrary/test/route',
			});
		});

		test('with preexisting state', () => {
			expect(authenticationReducer({
				currentUser: 'test891234h',
				loading: false,
				error: null,
				token: 'randomtokenhere:)1234',
				nextRoute: '/',
			}, {
				type: 'AUTH_SET_ROUTE_AFTER_AUTH',
				route: '/arbitrary/test/route2',
			})).toMatchObject({
				currentUser: 'test891234h',
				loading: false,
				error: null,
				token: 'randomtokenhere:)1234',
				nextRoute: '/arbitrary/test/route2',
			});
		});
	});

	describe('START_LOGIN', () => {
		test('without existing state', () => {
			expect(authenticationReducer(undefined, {
				type: 'AUTH_START_LOGIN',
			})).toMatchObject({
				...authenticationReducer(undefined, {}),
				loading: true,
			});
		});

		test('with preexisting state', () => {
			expect(authenticationReducer({
				currentUser: 'test891234h',
				loading: false,
				error: null,
				token: 'randomtokenhere:)1234',
				nextRoute: '/',
			}, {
				type: 'AUTH_START_LOGIN',
			})).toMatchObject({
				currentUser: 'test891234h',
				loading: true,
				error: null,
				token: 'randomtokenhere:)1234',
				nextRoute: '/',
			});
		});
	});

	describe('LOGIN_SUCCESS', () => {
		test('without existing state', () => {
			expect(authenticationReducer(undefined, {
				type: 'AUTH_LOGIN_SUCCESS',
				data: {
					user: 'testuser123',
					token: 'testtoken09123',
				},
			})).toMatchObject({
				...authenticationReducer(undefined, {}),
				token: 'testtoken09123',
				loading: false,
				currentUser: 'testuser123',
			});
		});

		test('with preexisting state', () => {
			expect(authenticationReducer({
				currentUser: 'test891234h',
				loading: true,
				error: null,
				token: 'randomtokenhere:)1234',
				nextRoute: '/',
			}, {
				type: 'AUTH_LOGIN_SUCCESS',
				data: {
					user: 'testuser123',
					token: 'testtoken09123',
				},
			})).toMatchObject({
				error: null,
				token: 'testtoken09123',
				loading: false,
				currentUser: 'testuser123',
				nextRoute: '/',
			});
		});
	});

	describe('LOGIN_ERROR', () => {
		test('without existing state', () => {
			expect(authenticationReducer(undefined, {
				type: 'AUTH_LOGIN_ERROR',
				error: 'errormessageasdfgh',
			})).toMatchObject({
				...authenticationReducer(undefined, {}),
				token: null,
				loading: false,
				error: 'errormessageasdfgh',
				currentUser: null,
			});
		});

		test('with preexisting state', () => {
			expect(authenticationReducer({
				currentUser: 'test891234h',
				loading: true,
				error: null,
				token: 'randomtokenhere:)1234',
				nextRoute: '/',
			}, {
				type: 'AUTH_LOGIN_ERROR',
				error: 'err89vbe',
			})).toMatchObject({
				nextRoute: '/',
				token: null,
				loading: false,
				error: 'err89vbe',
				currentUser: null,
			});
		});
	});

	describe('START_LOGOUT', () => {
		test('without existing state', () => {
			expect(authenticationReducer(undefined, {
				type: 'AUTH_START_LOGOUT',
			})).toMatchObject({
				...authenticationReducer(undefined, {}),
				loading: true,
			});
		});

		test('with preexisting state', () => {
			expect(authenticationReducer({
				currentUser: 'peanutEater1998',
				loading: false,
				error: null,
				token: 'asdfg:)1234',
				nextRoute: '/',
			}, {
				type: 'AUTH_START_LOGOUT',
			})).toMatchObject({
				currentUser: 'peanutEater1998',
				error: null,
				token: 'asdfg:)1234',
				nextRoute: '/',
				loading: true,
			});
		});
	});

	describe('LOGOUT_SUCCESS', () => {
		test('without existing state', () => {
			expect(authenticationReducer(undefined, {
				type: 'AUTH_LOGOUT_SUCCESS',
			})).toMatchObject({
				...authenticationReducer(undefined, {}),
				token: null,
				currentUser: null,
				loading: false,
			});
		});

		test('with preexisting state', () => {
			expect(authenticationReducer({
				currentUser: 'RandomMockUser',
				loading: true,
				error: null,
				token: 'RandomMockTocken',
				nextRoute: '/',
			}, {
				type: 'AUTH_LOGOUT_SUCCESS',
			})).toMatchObject({
				error: null,
				nextRoute: '/',
				token: null,
				currentUser: null,
				loading: false,
			});
		});
	});

	describe('LOGOUT_ERROR', () => {
		test('without existing state', () => {
			expect(authenticationReducer(undefined, {
				type: 'AUTH_LOGOUT_ERROR',
				error: 'THIS IS AN ERROR! BE SCARED :)',
			})).toMatchObject({
				...authenticationReducer(undefined, {}),
				error: 'THIS IS AN ERROR! BE SCARED :)',
				loading: false,
			});
		});

		test('with preexisting state', () => {
			expect(authenticationReducer({
				currentUser: 'EvenMoreRandomMockToken',
				loading: true,
				error: null,
				token: 'EvenMoreRandomMockToken',
				nextRoute: '/',
			}, {
				type: 'AUTH_LOGOUT_ERROR',
				error: 'Random error to describe what went wrong',
			})).toMatchObject({
				currentUser: 'EvenMoreRandomMockToken',
				token: 'EvenMoreRandomMockToken',
				nextRoute: '/',
				error: 'Random error to describe what went wrong',
				loading: false,
			});
		});
	});
});
