/**
 * Created by nander on 5-12-17.
 */
import React from 'react';
import { connectMixin } from '../../core/stateRequirements';
import { currencies } from '../../state/money/currencies/actions';
import { connect } from 'react-redux';

class MoneyAmount extends React.Component {
	render() {
		if (!this.props.currencies.currencies)
			return <div>LOADING</div>;
		const cur = this.props.currencies.currencies.find(it => it.iso === this.props.money.currency);
		return <div>{cur.symbol} {Math.round(this.props.money.amount * 100) / 100}</div>;
	}
}

export default connect(
	state => ({ ...connectMixin({
		money: {
			currencies,
		}, state,
	}),
	currencies: state.money.currencies,
	})
)(MoneyAmount);
