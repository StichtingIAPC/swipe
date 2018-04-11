/* eslint-disable no-alert */
import React from 'react';
import { connect } from 'react-redux';

import { getPaymentsOnReceipt, getPaymentTypes, getIsPaymentSplit } from '../../../state/sales/payments/selectors';
import { getSalesTotal } from '../../../state/assortment/articles/selectors';
import {
	setAmountOfPaymentType as setPaymentTypeAction,
	toggleSplitPayment as toggleSplitPaymentAction,
	resetPaymentTypes as resetPaymentTypesAction,
} from '../../../state/sales/payments/actions';
import MoneyAmount from '../../money/MoneyAmount';
import { salesCommitCreate as salesCommitCreateAction } from '../../../state/sales/commit/actions';
import MoneyField from '../../forms/MoneyField';

function PaymentTypes(props) {
	const { paymentTypes, paymentTypesAmounts, isPaymentSplit, setPaymentType, resetPaymentTypes, salesCommitCreate, toggleSplitPayment, total } = props;

	if (paymentTypes === null) {
		return <div />;
	}

	return (
		<div className="row">
			<table>
				<tbody>
					<tr>
						{paymentTypes.map(paymentType => <td key={paymentType.id}>
							<button
								style={{ width: '100px' }}
								onClick={() => {
									resetPaymentTypes();
									setPaymentType(paymentType, {
										...total,
										amount: total.amount,
									});
								}}
								disabled={isPaymentSplit} >
								{paymentType.name}
							</button>
						</td>)}
						<td>
							<button
								onClick={() => {
									resetPaymentTypes();
									toggleSplitPayment();
								}} >
								split payment
							</button>
						</td>
					</tr>
					{isPaymentSplit ?
						<tr>
							{paymentTypes.map(paymentType => <td key={paymentType.id}>
								<MoneyField
									style={{ width: '100px' }}
									currency={'EUR'}
									onChange={amount => setPaymentType(paymentType, {
										...total,
										amount,
									})} />
							</td>)}
						</tr> :
						null}
					{/*<tr>*/}
						{/*{paymentTypes.map(paymentType =>*/}
							{/*<td key={paymentType.id} >*/}
								{/*<MoneyAmount*/}
									{/*money={paymentTypesAmounts[paymentType.id] || {*/}
										{/*amount: 0,*/}
										{/*currency: 'EUR',*/}
									{/*}} />*/}
							{/*</td>)}*/}
						{/*<td>*/}
							{/*{isPaymentSplit.toString()}*/}
						{/*</td>*/}
					{/*</tr>*/}
				</tbody>
			</table>
			<button onClick={() => salesCommitCreate()}>sell!</button>
		</div>
	);
}

export default connect(
	state => ({
		paymentTypes: getPaymentTypes(state),
		paymentTypesAmounts: getPaymentsOnReceipt(state),
		isPaymentSplit: getIsPaymentSplit(state),
		total: getSalesTotal(state),
	}),
	{
		setPaymentType: setPaymentTypeAction,
		resetPaymentTypes: resetPaymentTypesAction,
		salesCommitCreate: salesCommitCreateAction,
		toggleSplitPayment: toggleSplitPaymentAction,
		dispatch: args => args,
	}
)(PaymentTypes);
