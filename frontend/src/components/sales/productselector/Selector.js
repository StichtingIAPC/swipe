import React from 'react';
import { connect } from 'react-redux';
import { connectMixin, fetchStateRequirementsFor } from '../../../core/stateRequirements';

import { articles } from '../../../state/assortment/articles/actions';
import { stock } from '../../../state/stock/actions';
import { getStock } from '../../../state/assortment/articles/selectors';
import { mutateSalesLineOfArticle } from '../../../state/sales/sales/actions';
import SelectorLine from "./SelectorLine";

class Selector extends React.Component {
	componentWillMount() {
	}

	render() {
		const { stock } = this.props;

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
							<SelectorLine key={e.id} stockLine={e} />)}
					</tbody>
				</table>
			</div>
		);
	}
}

export default connect(
	state => ({
		stock: getStock(state),
	}),
	{
		addArticle: mutateSalesLineOfArticle,
		dispatch: args => args,
	}
)(Selector);
