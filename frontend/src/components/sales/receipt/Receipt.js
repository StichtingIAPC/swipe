import React from 'react';
import { connect } from 'react-redux';

import { currencies } from '../../../state/money/currencies/actions.js';
import { articles } from '../../../state/assortment/articles/actions';
import { stock } from '../../../state/stock/actions';
import PaymentTypes from './PaymentTypes';
import Customer from './Customer';
import SalesList from './SalesList';

class Receipt extends React.Component {
	componentWillMount() {
		fetchStateRequirementsFor(this);
	}

	render() {
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
			 stock: {
				 stock,
			 },

		 }, state
		),
		stock: state.stock.stock,
		state,
	})
)(Receipt);
