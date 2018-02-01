import React from 'react';
import { connect } from 'react-redux';
import { connectMixin, fetchStateRequirementsFor } from '../../../core/stateRequirements';

import { currencies } from '../../../state/money/currencies/actions.js';
import { articles } from '../../../state/assortment/articles/actions';
import { stock } from '../../../state/stock/actions';
import PaymentTypes from './PaymentTypes';
import Customer from './Customer';
import SalesList from './SalesList';

class Receipt extends React.Component {

	render() {
		return (
			<div className="row">
				<Customer />
				<SalesList />
				<PaymentTypes />


			</div>
		);
	}
}

export default connect(
	state => ({

		stock: state.stock.stock,
		state,
	})
)(Receipt);
