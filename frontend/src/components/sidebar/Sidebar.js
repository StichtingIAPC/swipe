import React from 'react';
import SBLink from './SideBarLink.js';
import auth from 'www/auth';

export default class Sidebar extends React.Component {
	render() {
		const login_logout = auth.isLoggedIn() ? (
			<SBLink to="/logout" text="Log out" glyph="log-out" />
		) : (
			<SBLink to="/login" text="Log in" glyph="log-in" />
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
