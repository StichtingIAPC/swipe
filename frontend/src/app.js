'use strict';

import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, IndexRedirect, IndexRoute, browserHistory } from 'react-router';

import Dashboard from './components/Dashboard.js';

class Application extends React.Component {
	render() {
		return <div className="swipe">{this.props.children}</div>;
	}
}

ReactDOM.render(
	<Router history={browserHistory}>
		<Route path="/" component={Application}>
			<IndexRedirect to="/dashboard" />
			<Route path="dashboard" component={Dashboard} />
		</Route>
	</Router>
, document.getElementById('app'));