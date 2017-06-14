import React from 'react';
import PropTypes from 'prop-types';

export default class DenominationCount extends React.PureComponent {
	static propTypes = {
		currency: PropTypes.shape({
			iso: PropTypes.string.isRequired,
			digits: PropTypes.number.isRequired,
			symbol: PropTypes.string.isRequired,
		}).isRequired,

		amount: PropTypes.string.isRequired,
		registerCount: PropTypes.shape({
			denomination_counts: PropTypes.arrayOf(PropTypes.shape({
				amount: PropTypes.string.isRequired,
				number: PropTypes.number.isRequired,
			})).isRequired,
		}).isRequired,

		disabled: PropTypes.bool.isRequired,
	};

	render() {
		const { currency, amount, registerCount, disabled } = this.props;

		return (
			<div className="input-group">
				<span className="input-group-addon">{currency.symbol} {(+amount).toFixed(currency.digits)}</span>
				<input
					disabled={disabled}
					className="form-control"
					type="number" min={0} step={1}
					onChange={evt => this.props.updateDenomAmount(amount, evt.target.value)}
					value={(registerCount.denomination_counts.find(count => count.amount === amount) || { number: 0 }).number} />
			</div>
		);
	}
}
