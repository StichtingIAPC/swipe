import React from 'react';
import SidebarLink from './SideBarLink.js';
import auth from 'www/auth';

export default class Sidebar extends React.Component {
	render() {
		const login_logout = auth.isLoggedIn() ? (
			<SidebarLink to="/logout" text="Log out" glyph="log-out" />
		) : (
			<SidebarLink to="/login" text="Log in" glyph="log-in" />
		);

		return (
			<aside className="main-sidebar">
				<section className="sidebar">
					<ul className="sidebar-menu">
						<SidebarLink to="/logistics/" text="Logistics" icon="barcode" />
						<SidebarLink to="/register/" text="Register" icon="euro" />
						<SidebarLink to="/pos/" text="POS" icon="calculator" />
						<SidebarLink to="/conf/" text="Admin" icon="gear">
							<SidebarLink to="/conf/register/" text="Registers" />
							<SidebarLink to="/conf/users/" text="Users" />
							<SidebarLink to="/conf/foo/" text="Foo">
								<SidebarLink to="/conf/bar/" text="Bar">
									<SidebarLink to="/conf/foo/baz" text="Baz" />
								</SidebarLink>
							</SidebarLink>
						</SidebarLink>
						<li><br /></li>
						{login_logout}
					</ul>
				</section>
			</aside>
		);
	}
}
