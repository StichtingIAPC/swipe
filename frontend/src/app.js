'use strict';
// System dependencies
import React from "react";
import ReactDOM from "react-dom";
import {createStore, applyMiddleware, compose} from "redux";
import {Provider} from "react-redux";
import createSagaMiddleware from "redux-saga";
import Routes from "./Routes.js";
import {browserHistory} from "react-router";
import {syncHistoryWithStore, routerMiddleware} from "react-router-redux";
import "./jQueryFix.js";
import "font-awesome/css/font-awesome.min.css";
import "./styles/main.scss";
import "bootstrap/dist/css/bootstrap.min.css";
import "admin-lte/dist/css/AdminLTE.min.css";
import "admin-lte/dist/css/skins/skin-blue.min.css";
// Pages
import rootReducer from "./reducers/root";
import saga from "./saga.js";

// Set up the Redux store
const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
const sagaMiddleware = createSagaMiddleware();
const store = createStore(
	rootReducer,
	composeEnhancers(applyMiddleware(routerMiddleware(browserHistory), sagaMiddleware))
);

export const getState = store.getState.bind(store);

// Run the main saga
sagaMiddleware.run(saga);

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
if (module.hot) module.hot.accept('./components/Application.js', render);
