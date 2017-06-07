import React from "react";
import { connect } from "react-redux";
// Actions
import { toggleSidebar } from "actions/sidebar.js";
// Components
import Topbar from "components/base/topbar/Topbar.js";
import Sidebar from "components/base/sidebar/Sidebar.js";

class Application extends React.Component {
	render() {
		return (
			<div className={`wrapper fixed${this.props.sidebarOpen ? ' sidebar-collapse sidebar-mini' : ' sidebar-open'}`}>
				<Topbar name={this.props.name} sidebarToggle={this.props.toggleSidebar} />
				<Sidebar />
				<div className="content-wrapper">
					<div className="content">
						{this.props.children}
					</div>
				</div>
			</div>
		);
	}
}

export default connect(
	state => ({ sidebarOpen: state.sidebar }),
	dispatch => ({ toggleSidebar: () => dispatch(toggleSidebar()) })
)(Application);
