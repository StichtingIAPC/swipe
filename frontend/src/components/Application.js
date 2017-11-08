import React from 'react';
import { connect } from 'react-redux';
import { Switch, Route } from 'react-router-dom';
// Actions
import { toggleSidebar } from '../state/sidebar/actions.js';
// Components
import Topbar from '../components/base/topbar/Topbar.js';
import Sidebar from '../components/base/sidebar/Sidebar.js';
import Dashboard from './Dashboard';
import HelloWorld from './HelloWorld';
import SupplierBase from './supplier/SupplierBase';
import MoneyBase from './money/MoneyBase';
import ArticleManager from './article/ArticleManager';
import RegisterBase from './register/RegisterBase';
import LabelsBase from './assortment/LabelsBase';

import { Switch, Route, Redirect } from 'react-router-dom';
import { push } from 'react-router-redux';
import { setRouteAfterAuthentication } from '../state/auth/actions.js';

// Subrouters
import { Error404 } from '../components/base/Error404';
import Dashboard from '../components/Dashboard.js';
import HelloWorld from '../components/HelloWorld.js';
// Supplier components
import SupplierBase from '../components/supplier/SupplierBase';
import SupplierEdit from '../components/supplier/SupplierEdit';
import SupplierDetail from '../components/supplier/SupplierDetail';
// Money components
import MoneyBase from '../components/money/MoneyBase';
import CurrencyDetail from '../components/money/currency/CurrencyDetail';
import CurrencyEdit from '../components/money/currency/CurrencyEdit';
import VATDetail from '../components/money/VAT/VATDetail';
import VATEdit from '../components/money/VAT/VATEdit';
import AccountingGroupEdit from '../components/money/accountingGroup/AccountingGroupEdit';
import AccountingGroupDetail from '../components/money/accountingGroup/AccountingGroupDetail';
// Article components
import ArticleEdit from '../components/article/ArticleEdit';
import ArticleManager from '../components/article/ArticleManager';
// Register components
import RegisterBase from '../components/register/RegisterBase';
import RegisterEdit from '../components/register/register/RegisterEdit';
import RegisterDetail from '../components/register/register/RegisterDetail';
import PaymentTypeEdit from '../components/register/paymentType/PaymentTypeEdit';
import PaymentTypeDetail from '../components/register/paymentType/PaymentTypeDetail';
import LabelsBase from '../components/assortment/LabelsBase';
import LabelTypeEdit from '../components/assortment/labeltype/LabelTypeEdit';
import UnitTypeEdit from '../components/assortment/unittype/UnitTypeEdit';
import LabelTypeDetail from '../components/assortment/labeltype/LabelTypeDetail';
import UnitTypeDetail from '../components/assortment/unittype/UnitTypeDetail';

class Application extends React.Component {
	render() {
		const { match } = this.props;
		return (
			<div
				className={`wrapper fixed${this.props.sidebarOpen ? ' sidebar-collapse sidebar-mini' : ' sidebar-open'}`}>
				<Topbar name={this.props.name} sidebarToggle={this.props.toggleSidebar} />
				<Sidebar />
				<div className="content-wrapper">
					<div className="content">
						<Switch>
							<Route path={`${match.path}/dashboard/`} component={Dashboard} />
							<Route path={`${match.path}/helloworld/`} component={HelloWorld} />
							<Route path={`${match.path}/supplier/`} component={SupplierBase} />
							<Route path={`${match.path}/money/`} component={MoneyBase} />
							<Route path={`${match.path}/articlemanager/`} component={ArticleManager} />
							<Route path={`${match.path}/register/`} component={RegisterBase} />
							<Route path={`${match.path}/assortment/`} component={LabelsBase} />
							<Route path="pos">
								<Switch>
									<Route path="register">
										<Switch>
											<Route path="state" />
											<Route path="open" />
											<Route path="close" />
											<Route path="/" strict={true}>
												<Redirect to="state" />
											</Route>
										</Switch>
									</Route>
									<Route path="/" strict={true}>
										<Redirect to="register" />
									</Route>
								</Switch>
							</Route>
							<Route path="*" component={Error404} />
						</Switch>
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
