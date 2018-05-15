import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';

import Big from 'big.js';

import MoneyField from '../../forms/MoneyField';
import { Col, Button, ButtonToolbar, FormGroup, HelpBlock } from 'react-bootstrap';
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


export default function PaymentTypes(props) {
	const { paymentTypes, paymentTypeAmounts, onPaymentTypeSet, onPaymentTypesReset, onToggleSplit, isSplit, salesTotal, validations } = props;
	const validation_total = validations ? validations.total : {};
	const totalValidationText = validation_total ? validation_total.text : '';
	const totalErrorType = validation_total ? validation_total.type : 'success';

	if (paymentTypeAmounts === null) {
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
								onPaymentTypesReset();
								onPaymentTypeSet(paymentType.id, {
									...salesTotal,
									amount: salesTotal.amount,
								});
							}}
							disabled={isSplit} >
							<FontAwesome icon={getIconForPaymentType(paymentType)} /> {paymentType.name}
						</Button >
					</Col >
				)}
				<Col md={3} >
					<Button
						block={true}
						onClick={() => {
							if (isSplit) {
								onPaymentTypesReset();
							}
							onToggleSplit();
						}} >
						<FontAwesome icon="th-list" /> split payment
					</Button >
				</Col >
			</ButtonToolbar >
			{isSplit ?
				<FormGroup
					controlId="formPaymentTypesSplit"
					validationState={totalErrorType}>
					<HelpBlock>{totalValidationText}</HelpBlock>
					{paymentTypes.map(paymentType =>
						<Col md={3} key={paymentType.id} >
							<ButtonToolbar block={true} >
								<Button
									onClick={() => {
										let amountLeft = new Big(salesTotal.amount)
											.minus(Object.values(paymentTypeAmounts).reduce(
												(sumBig, paymentTypeAmount) => sumBig.plus(paymentTypeAmount.amount), new Big(0))
											);

										if (amountLeft.lt(0)) {
											amountLeft = new Big(0);
										}

										const currentAmountPaymentType = paymentTypeAmounts[paymentType.id] ? new Big(paymentTypeAmounts[paymentType.id].amount) : new Big(0);

										onPaymentTypeSet(paymentType.id, {
											...salesTotal,
											amount: currentAmountPaymentType.plus(amountLeft).toFixed(5),
										});
									}} >
									<FontAwesome icon="arrow-down" /> Fill
								</Button >
								<Button
									onClick={() => {
										onPaymentTypeSet(paymentType.id, {
											...salesTotal,
											amount: 0,
										});
									}} >
									<FontAwesome icon="arrow-up" /> Empty
								</Button >
							</ButtonToolbar >
							<MoneyField
								currency={'EUR'}
								onChange={amount => onPaymentTypeSet(paymentType.id, {
									...salesTotal,
									amount,
								})}
								value={paymentTypeAmounts[paymentType.id] ? paymentTypeAmounts[paymentType.id].amount : '0'} />
						</Col >
					)
					}</FormGroup > : null}
		</div >
	);
}

PaymentTypes.propTypes = {
	onToggleSplit: PropTypes.func.isRequired,
	isSplit: PropTypes.bool.isRequired,
	onPaymentTypesReset: PropTypes.func.isRequired,
	onPaymentTypeSet: PropTypes.func.isRequired,
	paymentTypeAmounts: PropTypes.object.isRequired,
	salesTotal: PropTypes.string.isRequired,
	validations: PropTypes.object.isRequired,
	paymentTypes: PropTypes.array.isRequired,
};
