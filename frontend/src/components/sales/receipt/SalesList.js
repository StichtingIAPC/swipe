import React from 'react';
import { connect } from 'react-redux';
import { connectMixin, fetchStateRequirementsFor } from '../../../core/stateRequirements';
import { articles } from '../../../state/assortment/articles/actions';
import { mutateSalesLineOfArticle } from '../../../state/sales/sales/actions';
import { stock } from '../../../state/stock/actions';
import Totals from './Totals';
import SalesListLine from './SalesListLine';
import { Box } from 'reactjs-admin-lte';

class SalesList extends React.Component {

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
		sales: state.sales.sales,
	})
	,
	{
		addArticle: mutateSalesLineOfArticle,
		dispatch: args => args,
	}
)(SalesList);
