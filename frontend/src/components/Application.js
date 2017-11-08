import React from 'react';
import { connect } from 'react-redux';
// Actions
import { toggleSidebar } from '../state/sidebar/actions.js';
// Components
import Topbar from '../components/base/topbar/Topbar.js';
import Sidebar from '../components/base/sidebar/Sidebar.js';

class Application extends React.Component {
	render() {
		return (
			<div className={`wrapper fixed${this.props.sidebarOpen ? ' sidebar-collapse sidebar-mini' : ' sidebar-open'}`}>
				<Topbar name={this.props.name} sidebarToggle={this.props.toggleSidebar} />
				<Sidebar />
				<div className="content-wrapper">
					<div className="content">
						<Switch>
							<Route path="dashboard" component={Dashboard} />
							<Route path="helloworld" component={HelloWorld} />
							<Route path="supplier/" component={SupplierBase}>
								<Route path="create/" component={SupplierEdit} />
								<Route path=":supplierID/edit/" component={SupplierEdit} />
								<Route path=":supplierID/" component={SupplierDetail} />
							</Route>
							<Route path="money/" component={MoneyBase}>
								<Route path="currency/create/" component={CurrencyEdit} />
								<Route path="currency/:currencyID/edit/" component={CurrencyEdit} />
								<Route path="currency/:currencyID/" component={CurrencyDetail} />
								<Route path="vat/create/" component={VATEdit} />
								<Route path="vat/:VATID/edit/" component={VATEdit} />
								<Route path="vat/:VATID/" component={VATDetail} />
								<Route path="accountinggroup/create/" component={AccountingGroupEdit} />
								<Route path="accountinggroup/:accountingGroupID/edit/" component={AccountingGroupEdit} />
								<Route path="accountinggroup/:accountingGroupID/" component={AccountingGroupDetail} />
							</Route>
							<Route path="articlemanager/" component={ArticleManager}>
								<Route path="create/" component={ArticleEdit} />
								<Route path=":articleID/" component={ArticleEdit} />
							</Route>
							<Route path="register/" component={RegisterBase}>
								<Route path="register/create/" component={RegisterEdit} />
								<Route path="register/:registerID/edit/" component={RegisterEdit} />
								<Route path="register/:registerID/" component={RegisterDetail} />
								<Route path="paymenttype/create/" component={PaymentTypeEdit} />
								<Route path="paymenttype/:paymentTypeID/edit/" component={PaymentTypeEdit} />
								<Route path="paymenttype/:paymentTypeID/" component={PaymentTypeDetail} />
							</Route>
							<Route path="assortment" component={LabelsBase}>
								<Route path="labeltype/create/" component={LabelTypeEdit} />
								<Route path="labeltype/:labelTypeID/edit" component={LabelTypeEdit} />
								<Route path="labeltype/:labelTypeID/" component={LabelTypeDetail} />
								<Route path="unittype/create/" component={UnitTypeEdit} />
								<Route path="unittype/:unitTypeID/edit" component={UnitTypeEdit} />
								<Route path="unittype/:unitTypeID/" component={UnitTypeDetail} />
							</Route>
							<Route path="pos">
								<IndexRedirect to="register" />
								<Route path="register">
									<IndexRedirect to="state" />
									<Route path="state" />
									<Route path="open" />
									<Route path="close" />
								</Route>
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
