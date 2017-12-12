/**
 * Created by nander on 5-12-17.
 */
import React from 'react';
import PropTypes from 'prop-types';
import {connectMixin} from "../../core/stateRequirements";
import {currencies} from "../../state/money/currencies/actions";
import {connect} from "react-redux";

class MoneyAmount extends React.Component {

	render() {
		console.log(this.props.money);
		console.log(this.props.currencies)
		if (! this.props.currencies.currencies)
			return <div>LOADING</div>
		const cur = this.props.currencies.currencies.find(it => it.iso==this.props.money.currency);
		console.log(cur)
		return <div>{cur.symbol} {Math.round(this.props.money.amount * 100) / 100}</div>;
	}

}
export default connect(
	state => ({...connectMixin({
		money: {
			currencies,
		}, state,
	}),
	currencies: state.money.currencies,
	})
)(MoneyAmount);
