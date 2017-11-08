import React from 'react';
import { connect } from 'react-redux';
import { Switch, Route } from 'react-router-dom';
import { push } from 'react-router-redux';
import { setRouteAfterAuthentication } from './state/auth/actions.js';
// Subrouters
import Authentication from './components/authentication/Authentication.js';
import Application from './components/Application.js';

class Routes extends React.Component {
	checkAuthentication(nextState) {
		if (this.props.user === null)			{ this.props.authenticate(nextState.location.pathname); }
	}

	render() {
		return <Switch>
			<Route path="/authentication/login" component={Authentication} />
			<Route path="/" component={Application} />
		</Switch>;
	}
}

export default connect(
	state => ({ user: state.auth.currentUser }),
	dispatch => ({
		authenticate: route => {
			if (route !== null) { dispatch(setRouteAfterAuthentication(route)); }
			dispatch(push('/authentication/login'));
		},
	})
)(Routes);
