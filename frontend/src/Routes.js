import React from 'react';
import { connect } from 'react-redux';
import { Switch, Route } from 'react-router-dom';
import { push } from 'react-router-redux';
import { setRouteAfterAuthentication } from './state/auth/actions.js';
// Subrouters
import { Error404 } from './components/base/Error404';
import Authentication from './components/authentication/Authentication.js';
import Application from './components/Application.js';
import Dashboard from './components/Dashboard.js';
import HelloWorld from './components/HelloWorld.js';
// Supplier components
import SupplierBase from './components/supplier/SupplierBase';
import SupplierEdit from './components/supplier/SupplierEdit';
import SupplierDetail from './components/supplier/SupplierDetail';
// Money components
import MoneyBase from './components/money/MoneyBase';
import CurrencyDetail from './components/money/currency/CurrencyDetail';
import CurrencyEdit from './components/money/currency/CurrencyEdit';
import VATDetail from './components/money/VAT/VATDetail';
import VATEdit from './components/money/VAT/VATEdit';
import AccountingGroupEdit from './components/money/accountingGroup/AccountingGroupEdit';
import AccountingGroupDetail from './components/money/accountingGroup/AccountingGroupDetail';
// Article components
import ArticleEdit from './components/article/ArticleEdit';
import ArticleManager from './components/article/ArticleManager';
// Register components
import RegisterBase from './components/register/RegisterBase';
import RegisterEdit from './components/register/register/RegisterEdit';
import RegisterDetail from './components/register/register/RegisterDetail';
import PaymentTypeEdit from './components/register/paymentType/PaymentTypeEdit';
import PaymentTypeDetail from './components/register/paymentType/PaymentTypeDetail';
import LabelsBase from './components/assortment/LabelsBase';
import LabelTypeEdit from './components/assortment/labeltype/LabelTypeEdit';
import UnitTypeEdit from './components/assortment/unittype/UnitTypeEdit';
import LabelTypeDetail from './components/assortment/labeltype/LabelTypeDetail';
import UnitTypeDetail from './components/assortment/unittype/UnitTypeDetail';

class Routes extends React.Component {
	checkAuthentication(nextState) {
		if (this.props.user === null)			{ this.props.authenticate(nextState.location.pathname); }
	}

	render() {
		return <Switch>
			<Route path="/authentication">
				<Route path="login" component={Authentication} />
			</Route>
			<Route path="/" component={Application} onEnter={::this.checkAuthentication}>
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
			</Route>
		</Switch>;
	}
}

export default connect(
	state => ({ user: state.auth.currentUser }),
	dispatch => ({
		authenticate: route => {
			if (route !== null) { dispatch(setRouteAfterAuthentication(route)); }
			dispatch(push('/authentication/login'));
		},
	})
)(Routes);
