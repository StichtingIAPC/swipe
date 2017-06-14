import React, {PropTypes} from "react";
import {connect} from "react-redux";
import {loginReset} from "../../../actions/auth";
import SidebarLink from "./SidebarLink";

class Sidebar extends React.Component {
	render() {
		return (
			<aside className="main-sidebar">
				<section className="sidebar">
					<ul className="sidebar-menu">
						<SidebarLink to="/pos/register/" text="Register" icon="shopping-cart" />
						<SidebarLink to="/supplier/" text="Supplier" icon="truck"  />
						<SidebarLink to="/money/" text="Money config" icon="money" />
						<li><br /></li>
						<SidebarLink onClick={this.props.logout} text="Log out" glyph="log-out" />
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
	state => ({ isAuthenticated: state.auth.user !== null }),
	dispatch => ({ logout: () => dispatch(loginReset())})
)(Sidebar);
