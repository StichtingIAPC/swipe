import React, { PropTypes } from 'react';
import { connect } from 'react-redux';

import SidebarLink from './SidebarLink';

class Sidebar extends React.Component {

	render() {
		/*const loginLogout = auth.isAuthenticated() ? (
			<SidebarLink onClick={auth.startLogout} text="Log out" glyph="log-out" />
		) : (
			<SidebarLink onClick={auth.startAuthentication} text="Log in" glyph="log-in" />
		);
*/
		return (
			<aside className="main-sidebar">
				<section className="sidebar">
					<ul className="sidebar-menu">
				{/*		<Authenticated><SidebarLink to="/pos/" text="Point of Sale" icon="shopping-basket"  /></Authenticated>
						<Authenticated forPermission="^logistics\." component={SidebarLink} to="/logistics/" text="Logistics" icon="truck">
							<Authenticated forPermission="^supplier\." component={SidebarLink} to="/supplier/" text="Suppliers" />
						</Authenticated>
						<Authenticated forPermission="superillegalstuff" component={SidebarLink} to="/logistics/" text="Logistics" icon="barcode" />
						<Authenticated component={'li'}><br /></Authenticated>
						{/*loginLogout*/}
					</ul>
				</section>
			</aside>
		);
	}
}

Sidebar.propTypes = {
	children: PropTypes.node,
};

Sidebar.defaultProps = {};

export default connect(
	state => ({ isAuthenticated: state.auth.user !== null })
)(Sidebar);
