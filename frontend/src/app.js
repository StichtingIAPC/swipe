'use strict';

// System dependencies
import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, IndexRedirect, IndexRoute, browserHistory, Link } from 'react-router';

// Styles
import fontAwesome from 'font-awesome/css/font-awesome.min.css';
import Styles from './styles/main.scss';

import jQuery from './jQueryFix.js';

// Our stylesheets

//import foundation_style from 'scss/www/framework.scss';
//import swipe_style from 'scss/www/main.scss';

import bootstrapCss from 'bootstrap/dist/css/bootstrap.min.css';
//import bootstrapJs from 'bootstrap/dist/js/bootstrap.min';

import templateCss from 'admin-lte/dist/css/AdminLTE.min.css';
import templateCssSkin from 'admin-lte/dist/css/skins/skin-blue.min.css';

//import templateJs from 'admin-lte/dist/js/app.min';

// Pages
import Dashboard from './components/Dashboard.js';
import { LoginScreen, LogoutScreen } from 'www/components/login/LoginScreen';
import { Error404 } from 'www/components/error';

import { RegisterState } from 'register/components/RegisterState';

import auth from 'www/auth';

// Components
import Topbar from './components/Topbar.js';
import { Sidebar, SBLink } from './components/Sidebar.js';
import Glyphicon from 'tools/components/Glyphicon';

class Application extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			sidebar_collapsed: false,
		}
	}

	sidebar_toggle() {
		this.setState({sidebar_collapsed: !this.state.sidebar_collapsed});
	}

	logout() {
		// TODO: implement
	}

	render() {
		return (
			<div className={'wrapper fixed' + (this.state.sidebar_collapsed ? ' sidebar-collapse sidebar-mini' : '')}>
				<Topbar name={this.props.name} user={auth.getUser()} sidebar_toggle={this.sidebar_toggle.bind(this)}/>
				<Sidebar>
					<SBLink to="/logistics/" text="Logistics" icon="barcode"/>
					<SBLink to="/register/" text="Register" icon="euro"/>
					<SBLink to="/pos/" text="POS" icon="calculator"/>
					<SBLink to="/conf/" text="Admin" icon="gear">
						<SBLink to="/conf/register/" text="Registers"/>
						<SBLink to="/conf/users/" text="Users"/>
						<SBLink to="/conf/foo/" text="Foo">
							<SBLink to="/conf/bar/" text="Bar">
								<SBLink to="/conf/foo/baz" text="Baz"/>
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
			<Route path="dashboard" component={Dashboard}/>
			<Route path="pos">
				<IndexRedirect to="register"/>
				<Route path="register">
					<IndexRedirect to="state"/>
					<Route path="state"/>
					<Route path="open"/>
					<Route path="close"/>
				</Route>
			</Route>
			<Route path="login" component={LoginScreen}/>
			<Route path="logout" component={LogoutScreen}/>
			<Route path="test" components={{
				name: "string",
				pages: [{
					app: Application,
					props: {}
				}, {
					app: Application,
					props: {}
				}]
			}}/>
			<Route path="*" component={Error404}/>
		</Route>
	</Router>
, document.getElementById('app'));
