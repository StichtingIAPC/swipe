import React from 'react';
import { connect } from 'react-redux';
import { Switch, Route, Redirect } from 'react-router-dom';
// Actions
import { toggleSidebar } from '../state/sidebar/actions.js';
// Components
import Topbar from '../components/base/topbar/Topbar.js';
import Sidebar from '../components/base/sidebar/Sidebar.js';

import { push } from 'react-router-redux';

// Subrouters
import { Error404 } from '../components/base/Error404';
import Dashboard from '../components/Dashboard.js';
import HelloWorld from '../components/HelloWorld.js';
import SupplierBase from '../components/supplier/SupplierBase';
import MoneyBase from '../components/money/MoneyBase';
import ArticleManager from '../components/article/ArticleManager';
import RegisterBase from '../components/register/RegisterBase';
import LabelsBase from '../components/assortment/LabelsBase';
import Profile from './authentication/Profile';
import SalesExp from './sales/SalesBase';
import Externalise from './logistics/Externalise';
import WaitForLogin from './authentication/WaitForLogin';

class Application extends React.Component {
	render() {
		const { match } = this.props;

		return (
			<WaitForLogin>
				<div
					className={`wrapper fixed${this.props.sidebarOpen ? ' sidebar-collapse sidebar-mini' : ' sidebar-open'}`}>
					<Topbar name={this.props.name} sidebarToggle={this.props.toggleSidebar} />
					<Sidebar />
					<div className="content-wrapper">
						<div className="content">
							<Switch>
								<Route path={`${match.path}dashboard`} component={Dashboard} />
								<Route path={`${match.path}helloworld`} component={HelloWorld} />
								<Route path={`${match.path}supplier`} component={SupplierBase} />
								<Route path={`${match.path}money`} component={MoneyBase} />
								<Route path={`${match.path}articlemanager`} component={ArticleManager} />
								<Route path={`${match.path}register`} component={RegisterBase} />
								<Route path={`${match.path}assortment`} component={LabelsBase} />
								<Route path={`${match.path}profile`} component={Profile} />
								<Route path={`${match.path}sales`} component={SalesExp} />
								<Route path={`${match.path}logistics/externalise`} component={Externalise} />

								{/* <Route path={`${match.path}/pos/register/state`} /> */}
								<Route component={Error404} />
							</Switch>
						</div>
					</div>
				</div>
			</WaitForLogin>
		);
	}
}

export default connect(
	state => ({ sidebarOpen: state.sidebar }),
	dispatch => ({ toggleSidebar: () => dispatch(toggleSidebar()) })
)(Application);
