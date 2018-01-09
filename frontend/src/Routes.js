import React from 'react';
import { hot } from 'react-hot-loader';
import { Switch, Route } from 'react-router-dom';
// Subrouters
import Authentication from './components/authentication/Authentication.js';
import Application from './components/Application.js';

class Routes extends React.Component {
	render() {
		return <Switch>
			<Route path="/authentication/login" component={Authentication} />
			<Route component={Application} />
		</Switch>;
	}
}

export default hot(module)(Routes);
