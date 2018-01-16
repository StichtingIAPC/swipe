import React from 'react';
import { connect } from 'react-redux';
import { connectMixin, fetchStateRequirementsFor } from '../../../core/stateRequirements';
import { registers } from '../../../state/register/registers/actions.js';

import { currencies } from '../../../state/money/currencies/actions.js';
import { paymentTypes } from '../../../state/register/payment-types/actions.js';
import { articles } from '../../../state/assortment/articles/actions';
import { stock } from '../../../state/stock/actions';
import { getArticleById } from '../../../state/assortment/articles/selectors';
import PaymentTypes from "./PaymentTypes";

class Customer extends React.Component {
	componentWillMount() {
		fetchStateRequirementsFor(this);
	}

	render() {
		const { state } = this.props;

		return (
			<div className="row">
				This component does not as of yet exist. Sorry.

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


		 }, state
		),
		state,
	})
)(Customer);