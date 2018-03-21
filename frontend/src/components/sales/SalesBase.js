import React from 'react';
import { registers as registersAction } from '../../state/register/registers/actions.js';
import { currencies as currenciesAction } from '../../state/money/currencies/actions.js';
import { paymentTypes as paymentTypesAction } from '../../state/register/payment-types/actions.js';
import { articles as articlesAction } from '../../state/assortment/articles/actions';
import { stock as stockAction } from '../../state/stock/actions';
import Selector from './productselector/Selector';
import Receipt from './receipt/Receipt';
import { connect } from 'react-redux';

class RegisterBase extends React.Component {
	componentWillMount() {
		this.props.getRegisters();
		this.props.getPaymentTypes();
		this.props.getCurrencies();
		this.props.getArticles();
		this.props.getStock();
	}

	render() {
		return (
			<div className="row">
				<div className="col-xs-6 col-md-6">
					<Selector />
				</div>
				<div className="col-xs-6 col-md-6">
					<Receipt />
				</div>
			</div>
		);
	}
}

export default connect(
	state => ({
		stock: state.stock.stock,
	}),
	dispatch => ({
		getRegisters: () => dispatch(registersAction()),
		getPaymentTypes: () => dispatch(paymentTypesAction()),
		getCurrencies: () => dispatch(currenciesAction()),
		getArticles: () => dispatch(articlesAction()),
		getStock: () => dispatch(stockAction()),
	})
)(RegisterBase);


function dispatchIfFalse(truth, func){
	if (truth())  func();
}