import React from "react";
import { connect } from "react-redux";
import { Router, Route, IndexRedirect } from "react-router";
import { push } from "react-router-redux";
import { setRouteAfterAuthentication } from "actions/auth.js";
// Subrouters
import { Error404 } from "./components/base/Error404";
import Authentication from "./components/authentication/Authentication.js";
import Application from "./components/Application.js";
import Dashboard from "./components/Dashboard.js";
import HelloWorld from "./components/HelloWorld.js";
// Supplier components
import SupplierBase from "components/supplier/SupplierBase";
import SupplierEdit from "components/supplier/SupplierEdit";
import SupplierDetail from "components/supplier/SupplierDetail";
// Money components
import MoneyBase from "./components/money/MoneyBase";
import CurrencyDetail from "./components/money/currency/CurrencyDetail";
import CurrencyEdit from "./components/money/currency/CurrencyEdit";
import VATDetail from "./components/money/VAT/VATDetail";
import VATEdit from "./components/money/VAT/VATEdit";
import AccountingGroupEdit from "./components/money/accountingGroup/AccountingGroupEdit";
import AccountingGroupDetail from "./components/money/accountingGroup/AccountingGroupDetail";

class Routes extends React.Component {
	checkAuthentication(nextState) {
		if (this.props.user === null) this.props.authenticate(nextState.location.pathname);
	}

	render() {
		return <Router history={this.props.history}>
			<Route path="/authentication">
				<Route path="login" component={Authentication} />
			</Route>
			<Route path="/" component={Application} onEnter={this.checkAuthentication.bind(this)}>
				<IndexRedirect to="/dashboard" />
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
			</Route>
		</Router>;
	}
}

export default connect(
	state => ({ user: state.auth.currentUser }),
	dispatch => ({
		authenticate: (route) => {
			if (route != null) dispatch(setRouteAfterAuthentication(route))
			dispatch(push('/authentication/login'));
		},
	})
)(Routes);
