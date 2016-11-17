'use strict';

// System dependencies
import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, IndexRedirect, browserHistory } from 'react-router';

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
import { LoginScreen, LogoutScreen } from 'www/components/login/LoginScreen';
import { Error404 } from 'www/components/error';
import auth from 'www/auth';

// Components
import Topbar from './components/topbar/Topbar.js';
import Sidebar from './components/sidebar/Sidebar.js';
import SBLink from './components/sidebar/SideBarLink.js';

class Application extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			sidebarCollapsed: false,
		};
	}

	sidebarToggle() {
		this.setState({ sidebarCollapsed: !this.state.sidebarCollapsed });
	}

	logout() {
		// TODO: implement
	}

	render() {
		return (
			<div className={'wrapper fixed' + (this.state.sidebarCollapsed ? ' sidebar-collapse sidebar-mini' : '')}>
				<Topbar name={this.props.name} user={auth.getUser()} sidebarToggle={this.sidebarToggle.bind(this)} />
				<Sidebar>
					<SBLink to="/logistics/" text="Logistics" icon="barcode" />
					<SBLink to="/register/" text="Register" icon="euro" />
					<SBLink to="/pos/" text="POS" icon="calculator" />
					<SBLink to="/conf/" text="Admin" icon="gear">
						<SBLink to="/conf/register/" text="Registers" />
						<SBLink to="/conf/users/" text="Users" />
						<SBLink to="/conf/foo/" text="Foo">
							<SBLink to="/conf/bar/" text="Bar">
								<SBLink to="/conf/foo/baz" text="Baz" />
							</SBLink>
						</SBLink>
					</SBLink>
				</Sidebar>
				<div className="content-wrapper">
					<div className="content">
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
			<Route path="pos">
				<IndexRedirect to="register" />
				<Route path="register">
					<IndexRedirect to="state" />
					<Route path="state" />
					<Route path="open" />
					<Route path="close" />
				</Route>
			</Route>
			<Route path="login" component={LoginScreen} />
			<Route path="logout" component={LogoutScreen} />
			<Route
				path="test" components={{
					name: 'string',
					pages: [{
						app: Application,
						props: {},
					}, {
						app: Application,
						props: {},
					}],
				}} />
			<Route path="*" component={Error404} />
		</Route>
	</Router>
	, document.getElementById('app')
);
