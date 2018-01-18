import React from 'react';
import { connect } from 'react-redux';
import { connectMixin, fetchStateRequirementsFor } from '../../../core/stateRequirements';
import { registers } from '../../../state/register/registers/actions.js';
import { currencies } from '../../../state/money/currencies/actions.js';
import { paymentTypes } from '../../../state/register/payment-types/actions.js';
import { articles } from '../../../state/assortment/articles/actions';
import { addToSalesListAction } from '../../../state/sales/sales/actions';
import { getArticleNameById, getCount, getStockForArticle } from '../../../state/assortment/articles/selectors';
import { stock } from '../../../state/stock/actions';
import Totals from './Totals';
import Box from '../../base/Box';
import MoneyAmount from '../../money/MoneyAmount';

class SalesList extends React.Component {
	componentWillMount() {
		fetchStateRequirementsFor(this);
	}

	render() {
		const {sales, requirementsLoaded, state, addToSalesListAction, addArticle} = this.props;

		return (
			<Box>
				<Box.Header
					title="List or Products"/>
				<div>
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
								<th>
									<span>Total Price</span>
								</th>

							</tr>
						</thead>
						<tbody>
							{sales.map(e =>
								<tr key={e} onClick={(evt) => addArticle(e, -1, getStockForArticle(state, e.article).count)}>
									<td>{getArticleNameById(state, e.article)}</td>
									<td>{e.count}</td>
									<td><MoneyAmount money={e.price}/></td>
									<td><MoneyAmount money={{...e.price, amount: e.price.amount * e.count}}/></td>
								</tr>)}
							<Totals/>
						</tbody>
					</table>
				</div>
			</Box>);
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
		sales: state.sales.sales.sales,
		state: state,
	})
	,
	{
		addArticle: addToSalesListAction,
		dispatch: args => args,
	}
)(SalesList);
