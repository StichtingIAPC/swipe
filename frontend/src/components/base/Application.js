import React, { PropTypes } from 'react';

import auth from '../../core/auth';

// Components
import Topbar from './topbar/Topbar';
import Sidebar from './sidebar/Sidebar';
import LoginModal from './auth/LoginModal';

/**
 * Created by Matthias on 18/11/2016.
 */

export class Application extends React.Component {
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
				<Topbar name={this.props.name} user={auth.getUser()} sidebarToggle={this.sidebarToggle.bind(this)} />
				<Sidebar />
				<div className="content-wrapper">
					<div className="content">
						{this.props.children}
					</div>
				</div>
				<LoginModal />
			</div>
		);
	}
}

Application.propTypes = {
	name: PropTypes.string,
	children: PropTypes.node.isRequired,
};

export default Application;
