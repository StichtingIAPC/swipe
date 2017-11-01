'use strict';

// System dependencies
import React from 'react';
import ReactDOM from 'react-dom';
import { applyMiddleware, compose, createStore } from 'redux';
import { Provider } from 'react-redux';
import createSagaMiddleware from 'redux-saga';
import Routes from './Routes.js';
import { browserHistory } from 'react-router';
import { routerMiddleware, syncHistoryWithStore } from 'react-router-redux';
import 'font-awesome/css/font-awesome.min.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'admin-lte/dist/css/AdminLTE.min.css';
import 'admin-lte/dist/css/skins/skin-blue.min.css';
import 'react-datepicker/dist/react-datepicker.css';
import './styles/main.scss';
// Pages
import rootReducer from './state/reducer.js';
import saga from './state/saga.js';
import * as auth from "./state/auth/actions";

// Set up the Redux store
const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
const sagaMiddleware = createSagaMiddleware();
const store = createStore(
	rootReducer,
	composeEnhancers(applyMiddleware(routerMiddleware(browserHistory), sagaMiddleware))
);

// Run the main saga
sagaMiddleware.run(saga);

// Check if there is auth info to be restored
if (window && window.localStorage && window.localStorage.getItem('LAST_LOGIN_SUCCESS_ACTION')) {
	try {
		store.dispatch(auth.loginRestore(JSON.parse(window.localStorage.getItem('LAST_LOGIN_SUCCESS_ACTION'))));
	} catch (e) {
		console.error(e);
	}
}

// Create enhanced history
const enhancedHistory = syncHistoryWithStore(browserHistory, store);

// Render function
function render() {
	ReactDOM.render(
		<Provider store={store}>
			<Routes history={enhancedHistory} />
		</Provider>
		, document.getElementById('app')
	);
}

// First render + register hot loader for hot reloading in a dev environment
render();
if (module.hot) {
	module.hot.accept('./components/Application.js', render);
}
