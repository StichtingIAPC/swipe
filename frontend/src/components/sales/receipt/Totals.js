import React from 'react';
import { connect } from 'react-redux';
import { connectMixin, fetchStateRequirementsFor } from '../../../core/stateRequirements';
import { registers } from '../../../state/register/registers/actions.js';

import { currencies } from '../../../state/money/currencies/actions.js';
import { paymentTypes } from '../../../state/register/payment-types/actions.js';
import { articles } from '../../../state/assortment/articles/actions';
import { addToSalesListAction } from '../../../state/sales/sales/actions';
import {getArticleNameById, getCount, getSalesTotal} from "../../../state/assortment/articles/selectors";
import {stock} from "../../../state/stock/actions";
import MoneyAmount from "../../money/MoneyAmount";

class SalesList extends React.Component {
	componentWillMount() {
		fetchStateRequirementsFor(this);
	}

	render() {
		const {sales, requirementsLoaded, state, addToSalesListAction, addArticle} = this.props;
		const total = getSalesTotal(state);
		total.currency = total.currency || "EUR";
		total.amount = total.amount || 0;
		return (

			<tr key = "TOTAL">
				<td>TOTAL</td>
				<td></td>
				<td></td>
				<td><MoneyAmount money={total}/></td>
			</tr>
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
		sales: state.sales.sales.sales,
		state: state,
	})
	,{ addArticle:  (evt, count) => addToSalesListAction(evt, count), dispatch: args => args }

)(SalesList);
