import React from 'react';
import { connect } from 'react-redux';
import { connectMixin, fetchStateRequirementsFor } from '../../../core/stateRequirements';
import { registers } from '../../../state/register/registers/actions.js';

import { currencies } from '../../../state/money/currencies/actions.js';
import { paymentTypes } from '../../../state/register/payment-types/actions.js';
import { articles } from '../../../state/assortment/articles/actions';
import { stock } from '../../../state/stock/actions';
import {getPaymentTypes} from "../../../state/sales/payments/selectors";

class PaymentTypes extends React.Component {
	componentWillMount() {
		fetchStateRequirementsFor(this);
	}

	render() {
		const {  paymentTypes} = this.props;
		if (paymentTypes == null)
			 return null;
		return (
			<div className="row">
				{paymentTypes.map(e => <div key={e.id} className="col-xs-12 col-md-12">{e.name}</div>)}
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
		 }, state
		),
		paymentTypes: getPaymentTypes(state),
	})
)(PaymentTypes);
