import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { logout as doLogout } from '../../../state/auth/actions';
import SidebarLink from './SidebarLink';
import RegisterOpenIndicator from '../../register/RegisterOpenIndicator';

class Sidebar extends React.Component {
	render() {
		return (
			<aside className="main-sidebar">
				<section className="sidebar">
					<ul className="sidebar-menu">
						<SidebarLink text="Sales" icon="shopping-cart" to="/sales/" indicator={<RegisterOpenIndicator />} />

						<SidebarLink text="Article manager" icon="cube" to="/articlemanager/" />
						<SidebarLink text="Admin">
							<SidebarLink text="Supplier" icon="truck" to="/supplier/" />
							<SidebarLink text="Money config" icon="money" to="/money/" />
							<SidebarLink text="Register" icon="credit-card" to="/register/" />
							<SidebarLink text="Labels" icon="tag" to="/assortment/" />
						</SidebarLink>
						<li><br /></li>
						<SidebarLink onClick={this.props.logout} text="Log out" glyph="log-out" />
					</ul>
				</section>
			</aside>
		);
	}
}

Sidebar.propTypes = { children: PropTypes.node };

Sidebar.defaultProps = {};

export default connect(
	state => ({ isAuthenticated: state.auth.user !== null }),
	dispatch => ({ logout: () => dispatch(doLogout()) })
)(Sidebar);
