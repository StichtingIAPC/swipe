'use strict';

// System dependencies
import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, IndexRedirect, IndexRoute, browserHistory, Link } from 'react-router';

// Styles
import fontAwesome from 'font-awesome/css/font-awesome.min.css';
import jQuery from './jQueryFix.js';

// Our stylesheets
import foundation_style from 'scss/www/framework.scss';
import swipe_style from 'scss/www/main.scss';

// Pages
import Dashboard from './components/Dashboard.js';
import { LoginScreen, LogoutScreen } from 'www/components/login/LoginScreen';


// Components
import Topbar from './components/Topbar.js';
import Sidebar from './components/Sidebar.js';
import Glyphicon from 'tools/components/Glyphicon';

class Application extends React.Component {
	logout() {
		// TODO: implement
	}

	render() {
		return (
			<div className="container horizontal grow">
				<Sidebar>
					<Link to="#">Logistics <Glyphicon glyph="barcode" x-class="side-bar-icon"/></Link>
					<Link to="#">Register <Glyphicon glyph="inbox" x-class="side-bar-icon"/></Link>
					<Link to="#">POS <Glyphicon glyph="list-alt" x-class="side-bar-icon"/></Link>
				</Sidebar>
				<div className="sidebar-padding"></div>
				<div id="page-container">
					<Topbar/>
					<div className="topbar-padding"></div>
					<div className="page-content-container container grow">
						{this.props.children}
					</div>
				</div>
			</div>
		);
	}
}

ReactDOM.render(
	<Router history={browserHistory}>
		<Route path="/" component={Application}>
			<IndexRedirect to="/dashboard" />
			<Route path="dashboard" component={Dashboard} />
			<Route path="login" component={LoginScreen} />
			<Route path="logout" component={LogoutScreen} />
		</Route>
	</Router>
, document.getElementById('app'));