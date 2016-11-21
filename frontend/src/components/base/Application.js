import React, { PropTypes } from 'react';

import auth from '../../core/auth';

// Components
import Topbar from './topbar/Topbar';
import Sidebar from './sidebar/Sidebar';
import SBLink from './sidebar/SideBarLink';
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
				<Sidebar>
					<SBLink to="/supplier/" text="Supplier" icon="truck" />
					<SBLink to="/logistics/" text="Logistics" icon="barcode" />
					<SBLink to="/register/" text="Register" icon="euro" />
					<SBLink to="/pos/" text="POS" icon="calculator" />
					<SBLink to="/conf/" text="Admin" icon="gear">
						<SBLink to="/conf/register/" text="Registers" />
						<SBLink to="/conf/users/" text="Users" />
						<SBLink to="/conf/foo/" text="Foo">
							<SBLink to="/conf/bar/" text="Bar">
								<SBLink to="/conf/foo/baz" text="Baz" />
							</SBLink>
						</SBLink>
					</SBLink>
				</Sidebar>
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
