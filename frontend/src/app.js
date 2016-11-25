'use strict';

// System dependencies
import React, { PropTypes } from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, IndexRedirect, browserHistory } from 'react-router';
import { createStore, applyMiddleware } from 'redux';
import thunkMiddleware from 'redux-thunk'
import { Provider } from 'react-redux';

import './jQueryFix.js';

// Styles
import 'font-awesome/css/font-awesome.min.css';
import './styles/main.scss';

// Our stylesheets
import 'bootstrap/dist/css/bootstrap.min.css';
import 'admin-lte/dist/css/AdminLTE.min.css';
import 'admin-lte/dist/css/skins/skin-blue.min.css';

// Pages
import Dashboard from './components/Dashboard.js';
import { Error404 } from 'www/components/error';
import { Application } from './components/base/Application';
import rootReducer from './reducers/root';
import auth from './core/auth';

// Routes
import SupplierRoute from './routing/SupplierRoutes';
import { populateSuppliers } from './actions/suppliers';

const store = createStore(
	rootReducer,
	applyMiddleware(
		thunkMiddleware
	)
);

auth.initialize(store);

console.log(store);
store.dispatch(populateSuppliers());

ReactDOM.render(
	<Provider store={store}>
		<Router history={browserHistory}>
			<Route path="/" component={Application}>
				<IndexRedirect to="/dashboard" />
				<Route path="dashboard" component={Dashboard} />
				{SupplierRoute}
				<Route path="pos">
					<IndexRedirect to="register" />
					<Route path="register">
						<IndexRedirect to="state" />
						<Route path="state" />
						<Route path="open" />
						<Route path="close" />
					</Route>
				</Route>
				<Route path="*" component={Error404} />
			</Route>
		</Router>
	</Provider>
	, document.getElementById('app')
);
