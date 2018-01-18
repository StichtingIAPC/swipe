import React from 'react';
import { connect } from 'react-redux';
import { connectMixin, fetchStateRequirementsFor } from '../../../core/stateRequirements';
import { registers } from '../../../state/register/registers/actions.js';

import { currencies } from '../../../state/money/currencies/actions.js';
import { paymentTypes } from '../../../state/register/payment-types/actions.js';
import { articles } from '../../../state/assortment/articles/actions';
import { stock } from '../../../state/stock/actions';
import { getArticleNameById, getCount, getStockForArticle } from '../../../state/assortment/articles/selectors';
import { addToSalesListAction } from '../../../state/sales/sales/actions';
import MoneyAmount from '../../money/MoneyAmount';

class Selector extends React.Component {
	componentWillMount() {
		fetchStateRequirementsFor(this);
	}

	render() {
		const { stock, state, addArticle } = this.props;

		if (!stock)
			return null;
		return (
			<div className="row">
				<table className="table table-striped">
					<thead>
						<tr>
							<th>
								<span>Product</span>
							</th>
							<th>
								<span>Count</span>
							</th>
							<th>
								<span>Price per</span>
							</th>
						</tr>
					</thead>
					<tbody>
						{stock.map(e =>
							<tr key={e} onClick={(evt) => addArticle(e, 1, getStockForArticle(state, e.article).count)}>
								<td>{getArticleNameById(state, e.article)}</td>
								<td>{getCount(state, e)}</td>
								<td><MoneyAmount money={e.price}/></td>
							</tr>)}
					</tbody>
				</table>
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
			 stock: {
				 stock,
			 },

		 }, state
		),
		stock: state.stock.stock,
		state: state,
	}),
	{
		addArticle: addToSalesListAction,
		dispatch: args => args,
	}
)(Selector);
