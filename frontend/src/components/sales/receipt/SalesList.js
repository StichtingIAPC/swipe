import React from 'react';
import { connect } from 'react-redux';
import { connectMixin, fetchStateRequirementsFor } from '../../../core/stateRequirements';
import { articles } from '../../../state/assortment/articles/actions';
import { addToSalesListAction } from '../../../state/sales/sales/actions';
import { stock } from '../../../state/stock/actions';
import Totals from './Totals';
import Box from '../../base/Box';
import SalesListLine from './SalesListLine';

class SalesList extends React.Component {
	componentWillMount() {
		fetchStateRequirementsFor(this);
	}

	render() {
		const { sales } = this.props;

		return (
			<Box>
				<Box.Header
					title="List or Products" />
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
								<SalesListLine key={e.article} stockLine={e} />)}
							<Totals />
						</tbody>
					</table>
				</div>
			</Box>);
	}
}

export default connect(
	state => ({
		...connectMixin({
			article: {
				articles,
			},
			stock: {
				stock,
			},
		}, state
		),
		sales: state.sales.sales,
	})
	,
	{
		addArticle: addToSalesListAction,
		dispatch: args => args,
	}
)(SalesList);
