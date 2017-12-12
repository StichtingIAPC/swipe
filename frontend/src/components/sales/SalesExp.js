import React from 'react';
import {connect} from 'react-redux';
import {connectMixin, fetchStateRequirementsFor} from '../../core/stateRequirements';
import {registers} from '../../state/register/registers/actions.js';

import {currencies} from '../../state/money/currencies/actions.js';
import {paymentTypes} from '../../state/register/payment-types/actions.js';
import {articles} from '../../state/assortment/articles/actions';
import {stock} from '../../state/stock/actions';
import {getArticleById} from "../../state/assortment/articles/selectors";
import Selector from "./productselector/Selector";
import Receipt from "./receipt/Receipt";

class RegisterBase extends React.Component {
	componentWillMount() {
		fetchStateRequirementsFor(this);
	}

	render() {
		const {stock, state} = this.props;
		return (
			<div className="row">
				<div className="col-xs-6 col-md-6">
					<Selector />
				</div>
				<div className="col-xs-6 col-md-6">
					<Receipt />
				</div>
				<div className="col-xs-6 col-md-8">
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
			}, sales: {
				stock,
			},
		}, state
		),
		stock: state.stock.stock,
		state: state,
	})
)(RegisterBase);
