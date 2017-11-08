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
			<Route path="/authentication/login" component={Authentication} />
			<Route path="/" component={Application} />
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
