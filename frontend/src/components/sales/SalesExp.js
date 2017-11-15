import React from 'react';
import { connect } from 'react-redux';
import { connectMixin, fetchStateRequirementsFor } from '../../core/stateRequirements';
import { registers } from '../../state/register/registers/actions.js';

import { currencies } from '../../state/money/currencies/actions.js';
import { paymentTypes } from '../../state/register/payment-types/actions.js';
import { articles } from '../../state/assortment/articles/actions';
import { stock } from '../../state/sales/stock/actions';
import {getArticleById} from "../../state/assortment/articles/selectors";

class RegisterBase extends React.Component {
	componentWillMount() {
		fetchStateRequirementsFor(this);
	}

	render() {
		const {stock, state} = this.props;
		console.log(stock)
		return (
			<div className="row">
				<div className="col-xs-12 col-md-12">
					{stock.map(e => getArticleById(state, e.article).name + ": " + e.count + " FOR " + e.price.amount + " " + e.price.currency)}
				</div>
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
			 register: {
				 registers,
				 paymentTypes,
			 },
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
		state: state,
	})
)(RegisterBase);
