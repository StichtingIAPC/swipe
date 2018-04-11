import React from 'react';
import fetchAllCurrencies from '../../state/money/currencies/actions';
import { connect } from 'react-redux';
import numeral from 'numeral';
// Numeral is a library for parsing text representations of
// numbers and formatting numbers as text

/**
 * Created by Matthias on 30/11/2016.
 */


function getFormat(currency, hasThousandsSeparator) {
	let format = '0';

	if (hasThousandsSeparator) {
		format += ',0';
	}
	if (currency.digits > 0) {
		format = `${format}.${'0'.repeat(currency.digits)}`;
	}
	return format;
}

export class MoneyField extends React.Component {
	constructor(props) {
		super(props);

		this.state = {};

		this.handleChange = this.handleChange.bind(this);
		this.handleBlur = this.handleBlur.bind(this);
	}


	componentWillReceiveProps(nextProps) {
		if (!this.props.currencies) {
			this.setState({
				displayFormat: getFormat(this.props.currency, true), // Format used for displaying the value to the user (1,000.0)
				format: getFormat(this.props.currency, false), // Format used to store the value. (1000.0)
			});
			if (this.props.value === '') {
				this.setState({
					displayString: '', // String storing the string currently displaying
				});
			} else {
			// Converts the value passed on to a number, and formats it for displaying
				this.setState({
					displayString: numeral(this.props.value).format(this.state.displayFormat),
				});
			}
		}
		if (nextProps.currency !== this.props.currency) {
			this.setState({ displayFormat: getFormat(nextProps.currency, true) });
		}
	}


	handleChange(event) {
		const newValue = event.target.value;

		this.setState({ displayString: newValue }, () =>
			this.props.onChange(numeral(newValue)
				.format(this.state.format))); // Reformats the value for storing and passes on
	}

	handleBlur() {
		// On lost focus reformat the displayString for displaying
		this.setState({
			displayString: numeral(this.state.displayString).format(this.state.displayFormat),
		});
	}

	componentDidMount() {
		this.props.fetchCurrencies();
	}

	render() {
		let { currency } = this.props;
		const { currency: _, value, onChange, children, name, ...restProps } = this.props;

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
					{...restProps}
					type="text"
					className="form-control"
					value={this.state.displayString}
					name={name}
					onChange={this.handleChange}
					onBlur={this.handleBlur} />
				{children}
			</div>
		);
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
