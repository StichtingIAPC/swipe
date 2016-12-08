import React from 'react';
import { connect } from 'react-redux';
import { Router, Route, IndexRedirect } from 'react-router';
import { push } from 'react-router-redux';

import { setRouteAfterAuthentication } from 'actions/auth.js'

// Subrouters
import { Error404 } from './components/base/Error404';

import Authentication from './components/authentication/Authentication.js';
import Application from './components/Application.js';
import Dashboard from './components/Dashboard.js'
import HelloWorld from './components/HelloWorld.js';

class Routes extends React.Component {
	checkAuthentication(nextState, transition) {
		if (this.props.user === null) this.props.authenticate(nextState.location.pathname);
	}

	render() {
		return <Router history={this.props.history}>
			<Route path="/authentication">
				<Route path="login" component={Authentication} />
			</Route>
			<Route path="/" component={Application} onEnter={this.checkAuthentication.bind(this)}>
				<IndexRedirect to="/dashboard" />
				<Route path="dashboard" component={Dashboard} />
				<Route path="helloworld" component={HelloWorld} />

				{/*
				<Route path="pos">
					<IndexRedirect to="register" />
					<Route path="register">
						<IndexRedirect to="state" />
						<Route path="state" />
						<Route path="open" />
						<Route path="close" />
					</Route>
				</Route>*/}
				<Route path="*" component={Error404} />
			</Route>
		</Router>;
	}
}

export default connect(
	state => ({ user: state.auth.currentUser }),
	dispatch => ({
		authenticate: (route) => {
			if (route != null) dispatch(setRouteAfterAuthentication(route))
			dispatch(push('/authentication/login'));
		},
	})
)(Routes);
