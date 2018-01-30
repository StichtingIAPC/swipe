import React from 'react';
import { connect } from 'react-redux';
import { connectMixin, fetchStateRequirementsFor } from '../../../core/stateRequirements';

import { getSalesTotal } from '../../../state/assortment/articles/selectors';
import { stock } from '../../../state/stock/actions';
import MoneyAmount from '../../money/MoneyAmount';

export class Totals extends React.Component {
	render() {
		const { total } = this.props;
		if (!total)
			return null;
		return (

			<tr key = "TOTAL">
				<td>TOTAL</td>
				<td></td>
				<td></td>
				<td><MoneyAmount money={total} /></td>
			</tr>
		);
	}
}

export default connect(
	state => ({
		total: getSalesTotal(state),
	})
)(Totals);
