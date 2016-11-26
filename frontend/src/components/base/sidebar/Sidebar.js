import React, { PropTypes } from 'react';
import { connect } from 'react-redux';

import SidebarLink from './SidebarLink';
import Authenticated from '../auth/Authenticated';
import auth from '../../../core/auth';

let Sidebar = class extends React.Component {
	render() {
		const login_logout = auth.isAuthenticated() ? (
			<SidebarLink onClick={auth.startLogout} text="Log out" glyph="log-out" />
		) : (
			<SidebarLink onClick={auth.startAuthentication} text="Log in" glyph="log-in" />
		);

		return (
			<aside className="main-sidebar">
				<section className="sidebar">
					<ul className="sidebar-menu">
						<Authenticated component={SidebarLink} to="/pos/" text="Point of Sale" icon="shopping-basket" />
						<Authenticated forPermission="^logistics\." component={SidebarLink} to="/logistics/" text="Logistics" icon="truck">
							<Authenticated forPermission="^supplier\." component={SidebarLink} to="/supplier/" text="Suppliers" />
						</Authenticated>
						<Authenticated forPermission="superillegalstuff" component={SidebarLink} to="/logistics/" text="Logistics" icon="barcode" />
						<Authenticated component={'li'}><br /></Authenticated>
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

Sidebar.defaultProps = {};

Sidebar = connect(
	(state, ownProps) => ({
		...ownProps,
		isAuthenticated: state.auth.user !== null,
	})
)(Sidebar);

export {
	Sidebar,
}

export default Sidebar;
