import React from 'react';
import { connect } from 'react-redux';
import { connectMixin, fetchStateRequirementsFor } from '../../core/stateRequirements';
import { startFetchingRegisters } from '../../state/register/registers/actions.js';
import { currencies } from '../../state/money/currencies/actions.js';
import { startFetchingPaymentTypes } from '../../state/register/payment_types/actions.js';
import { articles } from '../../state/assortment/articles/actions';
import { stock } from '../../state/stock/actions';
import Selector from './productselector/Selector';
import Receipt from './receipt/Receipt';
import Customer from './receipt/Customer';
import PaymentTypes from './receipt/PaymentTypes';
import { Col, Row } from 'react-bootstrap';
import {
	getIsPaymentSplit,
	getPaymentsOnReceipt,
	getPaymentTypesTotalValidations
} from '../../state/sales/payments/selectors';
import { setCustomer } from '../../state/sales/actions';
import { getCustomer, getDummySalesTotal } from '../../state/sales/selectors';
import {
	resetAmountOfPaymentTypes,
	setAmountOfPaymentType,
	toggleSplitPayment
} from '../../state/sales/payments/actions';
import { addToSalesListAction, receiptAddProductAction } from '../../state/sales/sales/actions';
import { getActivePaymentTypes } from "../../state/register/payment_types/selectors";

class SalesBase extends React.Component {
	componentWillMount() {
		fetchStateRequirementsFor(this);
		this.props.fetchStock();
	}

	addArticle = (article, count) => {
		this.props.addProduct(article, count);
	};

	removeArticle = (article, count) => this.addArticle(article, -count);

	setCustomer = customer => {
		this.props.setCustomer(customer);
	};

	setPaymentTypes = paymentTypeDivision => {
		this.props.setPaymentTypes(paymentTypeDivision);
	};

	render() {
		return (
			<React.Fragment>
				<Row>
					<Col xs={12} md={12}>
						<Customer id="customer" onChange={this.setCustomer} customer={this.props.customer} />
					</Col>
				</Row>
				<Row>
					<Col xs={12} md={6}>
						<Selector onArticleAdd={this.addArticle} stock={this.props.stock} receipt={this.props.receipt} />
					</Col>
					<Col xs={12} md={6}>
						<Receipt onArticleRemove={this.removeArticle} receipt={this.props.receipt} />
					</Col>
				</Row>
				<Row>
					<Col xs={12} md={12}>
						<PaymentTypes
							isSplit={this.props.isSplit}
							onPaymentTypeSet={this.props.setAmountOfPaymentType}
							onPaymentTypesReset={this.props.resetAmountOfPaymentTypes}
							onToggleSplit={this.props.toggleSplitPayment}
							paymentTypeAmounts={this.props.paymentTypeAmounts}
							salesTotal={this.props.salesTotal}
							validations={this.props.validations}
							paymentTypes={this.props.paymentTypes} />
					</Col>
				</Row>
			</React.Fragment>
		);
	}
}

export default connect(
	state => ({
		...connectMixin({
			register: {
				startFetchingRegisters,
				startFetchingPaymentTypes,
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
		}, state),
		stock: state.stock.stock,
		paymentTypes: getActivePaymentTypes(state),
		paymentTypeAmounts: getPaymentsOnReceipt(state),
		isSplit: getIsPaymentSplit(state),
		salesTotal: getDummySalesTotal(state),
		validations: getPaymentTypesTotalValidations(state),
		customer: getCustomer(state),
		receipt: state.sales.sales,
		state,
	}),
	{
		setCustomer,
		setAmountOfPaymentType,
		resetAmountOfPaymentTypes,
		toggleSplitPayment,
		addSale: addToSalesListAction,
		addProduct: receiptAddProductAction,
		fetchStock: stock,
	}
)(SalesBase);
