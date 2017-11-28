import React from 'react';
import { connect } from 'react-redux';
import { connectMixin, fetchStateRequirementsFor } from '../../../core/stateRequirements';
import { registers } from '../../../state/register/registers/actions.js';

import { currencies } from '../../../state/money/currencies/actions.js';
import { paymentTypes } from '../../../state/register/payment-types/actions.js';
import { articles } from '../../../state/assortment/articles/actions';
import { stock } from '../../../state/sales/stock/actions';
import PaymentTypes from "./PaymentTypes";
import Customer from "./Customer";
import SalesList from "./SalesList";

class Receipt extends React.Component {
	componentWillMount() {
		fetchStateRequirementsFor(this);
	}

	render() {
		const { stock, state } = this.props;

		return (
			<div className="row">
				<Customer />
				<SalesList />
				<PaymentTypes />
				<div className="col-xs-8 col-md-8">
					{this.props.requirementsLoaded ? this.props.children : null}
				</div>

			</div>
		);
	}
}

export default connect(
	state => ({
		...connectMixin({
			 money: {
				 currencies,
			 },
			 article: {
				 articles,
			 },
			 sales: {
				 stock,
			 },

		 }, state
		),
		stock: state.sales.stock.stock,
		state,
	})
)(Receipt);
