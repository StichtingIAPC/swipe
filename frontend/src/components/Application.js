import React from 'react';
import { connect } from 'react-redux';
import { push } from 'react-router-redux';

// Components
import Topbar from 'components/base/topbar/Topbar.js';
import Sidebar from 'components/base/sidebar/Sidebar.js';

export default class Application extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			sidebarCollapsed: false,
		};
	}

	sidebarToggle() {
		this.setState({ sidebarCollapsed: !this.state.sidebarCollapsed });
	}

	render() {
		return (
			<div className={'wrapper fixed' + (this.state.sidebarCollapsed ? ' sidebar-collapse sidebar-mini' : ' sidebar-open')}>
				<Topbar name={this.props.name} sidebarToggle={this.sidebarToggle.bind(this)} />
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
