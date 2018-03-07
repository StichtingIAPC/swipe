import React from 'react';
import fetchAllCurrencies from '../../state/money/currencies/actions';
import { connect } from 'react-redux';

/**
 * Created by Matthias on 30/11/2016.
 */

export class MoneyField extends React.Component {
	componentDidMount() {
		this.props.fetchCurrencies();
	}

	render() {
		let { currency } = this.props;
		const { currency: _, value, onChange, children, name } = this.props;

		if (typeof currency === 'string') {
			const validCurrencies = this.props.currencies.filter(c => c.iso === currency);

			if (validCurrencies.length <= 0) {
				return <div />;
			}
			currency = validCurrencies[0];
		}
		return (
			<div className="input-group">
				<span className="input-group-addon">{currency.symbol}</span>
				<input
					type="text"
					className="form-control"
					value={MoneyField.valueToString(value, currency)}
					placeholder = {MoneyField.getPlaceholder(currency)}
					onChange={onChange}
					name={name} />
				{children}
			</div>
		);
	}

	static valueToString(value, currency) {
		if (isNaN(Number(value.replace('.', '')))) {
			return value;
		}

		let _value = value.replace('.', '');

		_value = Number(_value) / Math.pow(10, currency.digits);
		_value = _value === 0 ? '' : _value.toFixed(currency.digits);
		return _value;
	}

	static getPlaceholder(currency) {
		return `0.${'0'.repeat(currency.digits)}`;
	}
}

export default connect(
	state => ({
		currencies: state.money.currencies.currencies,
	}),
	{
		fetchCurrencies: fetchAllCurrencies,
	}
)(MoneyField);
