'use strict';

// System dependencies
import React from 'react';
import ReactDOM from 'react-dom';
import { AppContainer } from 'react-hot-loader';
import { Provider } from 'react-redux';
import Routes from './Routes.js';
import { ConnectedRouter, push } from 'react-router-redux';
import 'admin-lte/dist/css/AdminLTE.min.css';
import 'admin-lte/dist/css/skins/skin-blue.min.css';
import 'font-awesome/css/font-awesome.min.css';
import 'react-datepicker/dist/react-datepicker.css';
import 'react-select/dist/react-select.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import './styles/main.scss';
// Pages
import saga from './state/saga.js';
import * as auth from './state/auth/actions';

import store, { sagaMiddleware, history } from './state/store';
export { history };

sagaMiddleware.run(saga);

// Check if there is auth info to be restored
if (window && window.localStorage && window.localStorage.getItem('LAST_LOGIN_SUCCESS_ACTION')) {
	try {
		store.dispatch(auth.loginRestore(JSON.parse(window.localStorage.getItem('LAST_LOGIN_SUCCESS_ACTION'))));
	} catch (e) {
		console.error(e);
	}
} else {
	store.dispatch(push('/authentication/login'));
}

// Create enhanced history

// Render function
function render() {
	ReactDOM.render(
		<AppContainer>
			<Provider store={store}>
				<ConnectedRouter history={history}>
					<Routes />
				</ConnectedRouter>
			</Provider>
		</AppContainer>
		, document.getElementById('app')
	);
}

// First render + register hot loader for hot reloading in a dev environment
render();

if (module.hot) {
	module.hot.accept('./Routes.js', render);
}
