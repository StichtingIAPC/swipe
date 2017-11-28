import React from 'react';
import { connect } from 'react-redux';
import { connectMixin, fetchStateRequirementsFor } from '../../../core/stateRequirements';
import { registers } from '../../../state/register/registers/actions.js';

import { currencies } from '../../../state/money/currencies/actions.js';
import { paymentTypes } from '../../../state/register/payment-types/actions.js';
import { articles } from '../../../state/assortment/articles/actions';
import { stock } from '../../../state/sales/stock/actions';
import { getArticleNameById, getCount} from "../../../state/assortment/articles/selectors";
import {addToSalesListAction} from "../../../state/sales/sales/actions";

class Selector extends React.Component {
	componentWillMount() {
		fetchStateRequirementsFor(this);
	}

	render() {
		const {stock, state, addArticle} = this.props;
		if(!stock)
			return null;
		return (
			<div className="row">
				{stock.map(e => <div key={e.article} className="col-xs-12 col-md-12" onClick={(evt) => addArticle(e, 1)}>{getArticleNameById(state, e.article)}: {getCount(state, e)} FOR {e.price.amount} {e.price.currency}</div>)}
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
		stock: state.sales.stock.stock,
		state: state,
	})
	,{ addArticle:  (evt, count) => addToSalesListAction(evt, count), dispatch: args => args }

)(Selector);
