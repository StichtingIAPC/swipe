import React from 'react';
import { Switch, Route } from 'react-router-dom';
// Subrouters
import Authentication from './components/authentication/Authentication.js';
import Application from './components/Application.js';

export default class Routes extends React.Component {
	render() {
		return <Switch>
			<Route path="/authentication/login" component={Authentication} />
			<Route component={Application} />
		</Switch>;
	}
}
