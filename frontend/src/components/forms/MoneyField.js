import React from "react";

/**
 * Created by Matthias on 30/11/2016.
 */

export default class MoneyField extends React.Component {
	render() {
		const {currency, value, onChange, children, ...restProps} = this.props;
		return (
			<div className="input-group">
				<span className="input-group-addon">{currency.symbol}</span>
				<input
					type="text"
					className="form-control"
					value={this.valueToString(value, currency)}
					placeholder = {this.getPlaceholder(currency)}
					onChange={onChange}
					{...restProps} />
				{children}
			</div>
		)
	}

	valueToString(value, currency) {
		if (isNaN(Number(value.replace(".", "")))){
			return value;
		}
		let _value = value.replace(".", "");
		_value = (Number(_value) / Math.pow(10, currency.digits));
		_value = _value === 0 ? "" : _value.toFixed(currency.digits);
		return _value;
	}

	getPlaceholder(currency) {
		return "0." + ("0".repeat(currency.digits))
	}
}
