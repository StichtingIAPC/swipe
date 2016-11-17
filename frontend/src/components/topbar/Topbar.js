import React from 'react';
import auth from 'www/auth';
import UserBlock from './UserBlock.js';

export default class Topbar extends React.Component {
	render() {
		return (
			<header className="main-header">
				<a className="logo">
					<span className="logo-mini">👆ミ</span>
					<span className="logo-lg">Swipe</span>
				</a>
				<nav className="navbar navbar-static-top" role="navigation">
					<a className="sidebar-toggle" onClick={this.props.sidebarToggle} />
					<div className="navbar-custom-menu pull-left">
						<ul className="nav navbar-nav">
							<li>
								<a>{this.props.name || 'page'}</a>
							</li>
						</ul>
					</div>
					<div className="navbar-custom-menu">
						<ul className="nav navbar-nav">
							<UserBlock user={auth.getUser()} />
						</ul>
					</div>
				</nav>
			</header>
		);
	}
}
