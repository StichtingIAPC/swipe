import React from 'react';
import { connect } from 'react-redux';
import Big from 'big.js';

import {
	getPaymentsOnReceipt,
	getPaymentTypes,
	getIsPaymentSplit,
	getPaymentTypesTotalValidations
} from '../../../state/sales/payments/selectors';
import { getSalesTotal } from '../../../state/assortment/articles/selectors';
import {
	setAmountOfPaymentType as setPaymentTypeAction,
	toggleSplitPayment as toggleSplitPaymentAction,
	resetPaymentTypes as resetPaymentTypesAction,
} from '../../../state/sales/payments/actions';
import MoneyAmount from '../../money/MoneyAmount';
import { salesCommitCreate as salesCommitCreateAction } from '../../../state/sales/commit/actions';
import MoneyField from '../../forms/MoneyField';
import { Col, Button, ButtonToolbar, FormControl, FormGroup, HelpBlock } from 'react-bootstrap';
import FontAwesome from '../../tools/icons/FontAwesome';

function getIconForPaymentType(paymentType) {
	switch (paymentType.name) {
		case 'Cash':
			return 'money';
		case 'Maestro':
			return 'credit-card-alt';
		case 'Invoice':
			return 'file-text';
		default:
			return null;
	}
}


function PaymentTypes(props) {
	const { paymentTypes, paymentTypesAmounts, isPaymentSplit, setPaymentType, resetPaymentTypes, salesCommitCreate, toggleSplitPayment, total, validations } = props;
	const validation_total = validations ? validations.total : {};
	const totalValidationText = validation_total ? validation_total.text : '';
	const totalErrorType = validation_total ? validation_total.type : 'success';

	if (paymentTypes === null) {
		return <div />;
	}

	return (
		<div >
			<ButtonToolbar >
				{paymentTypes.map(paymentType =>
					<Col key={paymentType.id} md={3} >
						<Button
							bsStyle="primary"
							block={true}
							onClick={() => {
								resetPaymentTypes();
								setPaymentType(paymentType.id, {
									...total,
									amount: total.amount,
								});
							}}
							disabled={isPaymentSplit} >
							<FontAwesome icon={getIconForPaymentType(paymentType)} /> {paymentType.name}
						</Button >
					</Col >
				)}
				<Col md={3} >
					<Button
						block={true}
						onClick={() => {
							if (isPaymentSplit) {
								resetPaymentTypes();
							}
							toggleSplitPayment();
						}} >
						<FontAwesome icon="th-list" /> split payment
					</Button >
				</Col >
			</ButtonToolbar >
			{isPaymentSplit ?
				<FormGroup
					controlId="formPaymentTypesSplit"
					validationState={totalErrorType}>
					<HelpBlock>{totalValidationText}</HelpBlock>
					{paymentTypes.map(paymentType =>
						<Col md={3} key={paymentType.id} >
							<ButtonToolbar block={true} >
								<Button
									onClick={() => {
										let amountLeft = new Big(total.amount)
											.minus(Object.values(paymentTypesAmounts).reduce(
												(sumBig, paymentTypeAmount) => sumBig.plus(paymentTypeAmount.amount), new Big(0))
											);

										if (amountLeft.lt(0)) {
											amountLeft = new Big(0);
										}

										const currentAmountPaymentType = paymentTypesAmounts[paymentType.id] ? new Big(paymentTypesAmounts[paymentType.id].amount) : new Big(0);

										setPaymentType(paymentType.id, {
											...total,
											amount: currentAmountPaymentType.plus(amountLeft).toFixed(5),
										});
									}} >
									<FontAwesome icon="arrow-down" /> Fill
								</Button >
								<Button
									onClick={() => {
										setPaymentType(paymentType.id, {
											...total,
											amount: 0,
										});
									}} >
									<FontAwesome icon="arrow-up" /> Empty
								</Button >
							</ButtonToolbar >
							<MoneyField
								currency={'EUR'}
								onChange={amount => setPaymentType(paymentType.id, {
									...total,
									amount,
								})}
								value={paymentTypesAmounts[paymentType.id] ? paymentTypesAmounts[paymentType.id].amount : 0} />
						</Col >
					)
					}</FormGroup > : null}
			<button onClick={() => salesCommitCreate()} >sell!</button >
		</div >
	);
}

export default connect(
	state => ({
		paymentTypes: getPaymentTypes(state),
		paymentTypesAmounts: getPaymentsOnReceipt(state),
		isPaymentSplit: getIsPaymentSplit(state),
		total: getSalesTotal(state),
		validations: getPaymentTypesTotalValidations(state),
	}),
	{
		setPaymentType: setPaymentTypeAction,
		resetPaymentTypes: resetPaymentTypesAction,
		salesCommitCreate: salesCommitCreateAction,
		toggleSplitPayment: toggleSplitPaymentAction,
		dispatch: args => args,
	}
)(PaymentTypes);
