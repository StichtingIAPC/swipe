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


	static getDerivedStateFromProps(nextProps, prevState) {
		const nextState = {};

		if (nextProps.currencies) {
			if (typeof prevState.currency === 'undefined' || nextProps.currencyISO !== prevState.currency.iso) {
				nextState.currency = nextProps.currencies.find(c => c.iso === nextProps.currencyISO);
				nextState.displayFormat = getFormat(nextState.currency, true); // Format used for displaying the value to the user (1,000.0)
				nextState.format = getFormat(nextState.currency, false); // Format used to store the value. (1000.0)
				if (nextProps.value === '') {
					nextState.displayString = '';
				} else {
					nextState.displayString = numeral(nextProps.value).format(nextState.displayFormat);
				}
			}
		}
		return {
			...prevState,
			...nextState,
		};
	}

	componentWillReceiveProps(nextProps) {
		this.setState(MoneyField.getDerivedStateFromProps(nextProps, this.state));
	}

	handleChange(event) {
		const newValue = event.target.value;

		this.setState({ displayString: newValue }, () =>
			this.props.onChange(
				numeral(newValue).format(this.state.format))); // Reformats the value for storing and passes on
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
		const { currencyISO, fetchCurrencies, children, name, ...restProps } = this.props;

		if (typeof this.state.currency === 'undefined') {
			return <div />;
		}

		return (
			<div className="input-group">
				<span className="input-group-addon">{this.state.currency.symbol}</span>
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
