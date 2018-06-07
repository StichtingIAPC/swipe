/**
 * Created by nander on 5-12-17.
 */
import React from 'react';
import { connect } from 'react-redux';
import fetchAllCurrencies from '../../state/money/currencies/actions';

export class MoneyAmount extends React.Component {
	componentWillMount() {
		if (!this.props.currencies.populated) {
			this.props.fetchAllCurrencies();
		}
	}

	render() {
		if (!this.props.currencies.currencies) { return <div>LOADING</div>; }
		let cur = this.props.currencies.currencies.find(it => it.iso === this.props.money.currency);

		if (cur == null) { cur = { symbol: '¬' }; }
		if (!this.props.money) {
			return <div />;
		}
		return <div>{cur.symbol} {Math.round(this.props.money.amount * 100) / 100}</div>;
	}
}

export default connect(
	state => ({
		currencies: state.money.currencies,
	}),
	{ fetchAllCurrencies }
)(MoneyAmount);
