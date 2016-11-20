import React from 'react'
import autoBind from 'react-autobind'

import fetch from 'isomorphic-fetch';

import { AUTHENTICATING } from '../reducers/auth';
import {
	startAuthentication,
	stopAuthentication,
	failAuthentication,
	login,
} from '../actions/auth';

import { LoginModal } from '../components/base/auth/LoginModal';

/**
 * Created by Matthias on 06/11/2016.
 */

const BASE_URL = window.location.host + ':8000'; // default django port;

const TOKEN = Symbol('auth token');
const loginRequest = Symbol('loginRequest');
const logoutRequest = Symbol('logoutRequest');
const APIRequest = Symbol('APIRequest');

const loginAttempt = Symbol('loginAttempt');

const authenticate = Symbol('authenticate');
const authenticateForRequest = Symbol('authenticateForRequest');

class AuthenticationError extends Error {}

const getCredentials = Symbol('getCredentials');

const auth = new (class Auth {
	constructor() {
		this[TOKEN] = null;
		autoBind(this);
	}

	initialize(store) {
		auth.store = store;
	}

	startLogout() {
		auth[logoutRequest]();
	}

	/**
	 * Get something from an absolute API endpoint <url> with <options>. Accepts when
	 * authenticated and no errors, rejects when no authentication or errors.
	 *
	 * Eventually will try to automatically ask for elevated permissions if current
	 * permissions are not enough.
	 *
	 * @param {string} url
	 * @param {Object} options
	 */
	authenticatedRequest(url, options) {
		const retry = (err) => {
			if (err instanceof TypeError) {
				return Promise.reject(err); // reject network problems
			}
			return auth[authenticate]() // get someone to authenticate themself
				.then(
					(response) =>
						// then try to do the request with that one's permissions/token
						auth[APIRequest](url, {...options}, response.json().token));
		};

		return auth[APIRequest](url, {...options}, auth[TOKEN])
			.catch(retry)
			.catch(retry)
			.catch(retry); // Let 3 people try to do the request before the request fails.
	}

	/**
	 * Method called by LoginModal to post the credentials to auth module.
	 * The method then routes it to the current credentials requester.
	 *
	 * @param username
	 * @param password
	 */
	login({username, password}) {
		auth[getCredentials]({username, password});
	}

	/**
	 * Cancel the current login attempt streak.
	 */
	cancel(err) {
		auth[getCredentials] = null;
		auth.store.dispatch(stopAuthentication());
	}

	/**
	 * Method to use when you want to let someone log in, but don't really care about what happens afterwards.
	 */
	startAuthentication() {
		auth.store.dispatch(startAuthentication());
		auth[authenticate]()
			.then((response) => {
				const json = response.json();
				const user = {
					username: json.username,
					gravitarUrl: json.gravitarUrl,
					permissions: [...json.permissions],
				};
				auth[TOKEN] = json.token;
				auth.store.dispatch(login(user));
			})
			.catch((err) => auth.cancel(err));
	}

	/**
	 * Ask for someone's (valid) authentications. Private method, as this one does not open the modal.
	 * @returns {Promise<Response>}
	 */
	[authenticate]() {
		return auth[loginAttempt]()   // try once
			.catch(auth[loginAttempt])  // try twice
			.catch(auth[loginAttempt]); // try three times to log in. If someone didn't make this,
		// they should get a better password. There is also no timeout currently, but when
		// implemented that should be done server-side.
	}

	/**
	 * This method listens to inputs from the LoginModal and uses that input to try to get the user
	 * status from the web.
	 *
	 * @param {Error} err: optional error which was the reason this attempt is made
	 * @returns {Promise<Response>}
	 */
	[loginAttempt](err) {
		// if there is an error, handle it
		if (err !== undefined) {
			auth.store.dispatch(failAuthentication(err));
			if (err instanceof TypeError) {
				return Promise.reject(new TypeError(err)); // reject transmission errors
			}
		}
		return new Promise((accept) => {
			auth[getCredentials] = accept;
		}).then((creds) => auth[loginRequest](creds))
	}

	/**
	 * Private method to send credentials. This sends only one request, and will
	 * fail if credentials are incorrect, or network fails.
	 *
	 * @param {string} username
	 * @param {string} password
	 * @returns {Promise<Response>}
	 */
	[loginRequest]({username, password}) {
		// put username and password into a form
		const fData = new FormData();
		fData.append('username', username);
		fData.append('password', password);

		// and send it to /auth/ on the server origin (origin = protocol + hostname + port)
		return fetch(`${BASE_URL}/auth/`, {
			method: 'PUT',
			body: fData,
		}).then((response) => {
			// check if the response was successful
			if (response.ok) {
				return response;
			} else {
				// if it was not successful (response status not in range http 2xx), reject the request.
				return Promise.reject(new AuthenticationError(response));
			}
		})
	}

	/**
	 * Log out. Not binding, but a nice way to reject a token server-side.
	 *
	 * @returns {Promise<Response>}
	 */
	[logoutRequest]() {
		const fData = new FormData();
		fData.append('token', auth.token);
		return fetch(`${BASE_URL}/auth/logout/`, {
			method: 'POST',
			body: fData,
		}).then((response) => {
			if (response.ok) {
				return response;
			} else {
				return Promise.reject(response);
			}
		})
	}

	/**
	 * Call an API with authentication. PRIVATE USE ONLY. Injects the token into the options
	 * of a 'fetch', and then returns the result. Doesn't check for fails or whatever.
	 *
	 * @param {string} uri: the URI used for this request. e.g. /api/method/arg1/arg2/
	 * @param {Object} options: Options object used in this request
	 * @param {string} token: The token to use in this request
	 * @constructor
	 */
	[APIRequest](uri, options, token) {
		const _headers = new Headers(options.headers);
		_headers.set('Authorization', `Token ${token}`);
		return fetch(`${BASE_URL}${uri}`, {...options, headers: _headers});
	}

	/**
	 * Get the user that is currently logged in.
	 * @returns {null|{username, gravatarUrl, token}}
	 */
	getUser() {
		return auth.store.getState().auth.user;
	}

	/**
	 * Check if the state of the current user is authenticated
	 * @returns {boolean}
	 */
	isAuthenticated() {
		return auth.store.getState().auth.isAuthenticated;
	}
})();

export default auth;
