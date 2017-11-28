import React from 'react';
import { connect } from 'react-redux';
import { connectMixin, fetchStateRequirementsFor } from '../../../core/stateRequirements';
import { registers } from '../../../state/register/registers/actions.js';

import { currencies } from '../../../state/money/currencies/actions.js';
import { paymentTypes } from '../../../state/register/payment-types/actions.js';
import { articles } from '../../../state/assortment/articles/actions';
import { addToSalesListAction } from '../../../state/sales/sales/actions';
import { getArticleNameById, getCount} from "../../../state/assortment/articles/selectors";
import {stock} from "../../../state/sales/stock/actions";

class SalesList extends React.Component {
	componentWillMount() {
		fetchStateRequirementsFor(this);
	}

	render() {
		const {sales, requirementsLoaded, state, addToSalesListAction, addArticle} = this.props;

		return (
			<div className="row">
				{sales.map(e => <div key={e} className="col-xs-12 col-md-12" onClick={(evt) => addArticle(e, -1)}>{getArticleNameById(state, e.article)}: {e.count} FOR {e.price.amount} {e.price.currency}</div>)}
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
		sales: state.sales.sales.sales,
		state: state,
	})
	,{ addArticle:  (evt, count) => addToSalesListAction(evt, count), dispatch: args => args }

)(SalesList);
