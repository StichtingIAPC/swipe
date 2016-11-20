import React, { PropTypes } from 'react';
import SBLink from './SideBarLink.js';
import auth from '../../../core/auth';

export class Sidebar extends React.Component {
	login(evt) {
		evt.preventDefault();
		auth.startAuthentication.bind(auth)();
	}

	logout(evt) {
		evt.preventDefault();
		auth.startLogout.bind(auth)();
	}

	render() {
		const login_logout = auth.isAuthenticated() ? (
			<SBLink to="/" onClick={this.logout.bind(this)} text="Log out" glyph="log-out" />
		) : (
			<SBLink to="/" onClick={this.login.bind(this)} text="Log in" glyph="log-in" />
		);

		return (
			<aside className="main-sidebar">
				<section className="sidebar">
					<ul className="sidebar-menu">
						{this.props.children}
						<li><br /></li>
						{login_logout}
					</ul>
				</section>
			</aside>
		);
	}
}

Sidebar.propTypes = {
	children: PropTypes.node.isRequired,
};

export default Sidebar;
