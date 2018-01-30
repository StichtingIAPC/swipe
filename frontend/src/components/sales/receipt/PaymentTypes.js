/* eslint-disable no-alert */
import React from 'react';
import { connect } from 'react-redux';
import { connectMixin, fetchStateRequirementsFor } from '../../../core/stateRequirements';
import { registers } from '../../../state/register/registers/actions.js';

import { currencies } from '../../../state/money/currencies/actions.js';
import { paymentTypes } from '../../../state/register/payment-types/actions.js';

import { getPaymentsOnReceipt, getPaymentTypes } from '../../../state/sales/payments/selectors';
import { getSalesTotal } from '../../../state/assortment/articles/selectors';
import { addPaymentType } from '../../../state/sales/payments/actions';
import MoneyAmount from '../../money/MoneyAmount';
import {salesCommitCreate} from "../../../state/sales/commit/actions";

class PaymentTypes extends React.Component {
	componentWillMount() {
		fetchStateRequirementsFor(this);
	}

	render() {
		const { paymentTypes, paymentTypesAmounts, addPaymentType, salesCommitCreate, total } = this.props;

		if (paymentTypes === null) {
			return null;
		}
		const totalPaid = Object.keys(paymentTypesAmounts).reduce((x, y) => {
			console.log(x, y, paymentTypesAmounts[y]); return { ...x,
				amount: x.amount + paymentTypesAmounts[y].amount };
		}, { currency: 'EUR',
			amount: 0 });

		return (
			<div className="row">
				<table>
					{paymentTypes.map(e =>
						<tr key={e.id}>
							<td
								onClick={ () => addPaymentType(e, { ...total,
									amount: total.amount - totalPaid.amount })}>{e.name}</td>
							{<td><MoneyAmount
								money={paymentTypesAmounts[e.name] || { amount: 0,
									currency: 'EUR' }} /> </td>}</tr>)}
					<tr><td><emph>Remaining:</emph></td><td><emph><MoneyAmount
						money={{ ...total,
							amount: total.amount - totalPaid.amount }} /></emph></td></tr>
				</table>
				<div className="col-xs-8 col-md-8">
					{this.props.requirementsLoaded ? this.props.children : null}
				</div>
				<div onClick={() => salesCommitCreate()}>asdifjasdofjasdf asdfjpadj asdfjadf<br/>HI</div>
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
		paymentTypesAmounts: getPaymentsOnReceipt(state),
		total: getSalesTotal(state),
	}),
	{
		addPaymentType,
		salesCommitCreate,
		dispatch: args => args,
	}
)(PaymentTypes);
