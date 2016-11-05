'use strict';

// System dependencies
import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, IndexRedirect, IndexRoute, browserHistory, Link } from 'react-router';

// Styles
import fontAwesome from '../../node_modules/font-awesome/css/font-awesome.min.css';
import jQuery from './jQueryFix.js';

import bootstrapCss from '../../node_modules/bootstrap/dist/css/bootstrap.min.css'
import bootstrapJs from 'bootstrap';

import templateCss from '../../node_modules/admin-lte/dist/css/AdminLTE.min.css';
import templateCssSkin from '../../node_modules/admin-lte/dist/css/skins/skin-blue.min.css';
import templateJs from '../../node_modules/admin-lte/dist/js/app.min.js';

import StylesMain from './styles/main.scss';

// Pages
import Dashboard from './components/Dashboard.js';

class Application extends React.Component {
	logout() {
		// TODO: implement
	}

	render() {
		return <div className="wrapper fixed">
			<header className="main-header">
			

				<nav className="navbar navbar-static-top" role="navigation">
					<div className="container-fluid">
						<div className="navbar-header">
							<h1>Swipe</h1>
						</div>
						
						<div className="collapse navbar-collapse" id="navbar-collapse">
							<ul className="nav navbar-nav navbar-right">
								<li><a href="#">Link</a></li>

								<li className="dropdown">
									<a href="#" className="dropdown-toggle" data-toggle="dropdown">Dropdown <span className="caret"></span></a>
									<ul className="dropdown-menu" role="menu">
										<li><a href="#">Action</a></li>
										<li><a href="#">Another action</a></li>
										<li><a href="#">Something else here</a></li>
										<li className="divider"></li>
										<li><a href="#">Separated link</a></li>
									</ul>
								</li>
							</ul>
						</div>
					</div>
				</nav>
			</header>

			<div className="sidebar-wrapper">
				<div className="main-sidebar">
					<div className="sidebar">
						<form action="#" method="get" className="sidebar-form">
							<div className="input-group">
								<input type="text" name="q" className="form-control" placeholder="Search..." />
								<span className="input-group-btn">
									<button type="submit" name="search" id="search-btn" className="btn btn-flat"><i className="fa fa-search"></i></button>
								</span>
							</div>
						</form>
					
						<ul className="sidebar-menu">
							<li className="header">VerCie</li>
							<li><a href="#"><i className="fa fa-credit-card"></i> <span>Kassa</span></a></li>
							<li><a href="#"><i className="fa fa-truck"></i> <span>Bestellen</span></a></li>

							<li className="header">Logistiek</li>
							<li><a href="#"><i className="fa fa-cube"></i> <span>Inkoopboek</span></a></li>
						</ul>
					</div>
				</div>
			</div>

			<div className="content-wrapper">
				<div className="content">
					{this.props.children}
				</div>
			</div>
		</div>;
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