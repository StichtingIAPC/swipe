import React from 'react';
import fetchAllCurrencies from '../../state/money/currencies/actions';

import { connect } from 'react-redux';
import Card from '../base/Card';
import PropTypes from 'prop-types';
import { FormControl, FormGroup, InputGroup } from 'react-bootstrap';
import { getCurrencyByIso } from '../../state/money/currencies/selectors';

export class MoneyField extends React.Component {
	componentDidMount() {
		this.props.fetchCurrencies();
	}

	render() {
		return (
			<FormGroup>
				<InputGroup>
					<InputGroup.Addon>{this.props.currencyObj.symbol}</InputGroup.Addon>
					<FormControl
						type="text"
						value={this.props.value}
						onChange={event => this.props.onChange(event.target.value.replace(',', '.'))}
						name={this.props.name} />
				</InputGroup>
			</FormGroup>
		);
	}
}

export default connect(
	(state, props) => ({
		currencyObj: getCurrencyByIso(state, props.currency),
	}),
	{
		fetchCurrencies: fetchAllCurrencies,
	}
)(MoneyField);
Card.propTypes = {
	currency: PropTypes.string.isRequired,
	value: PropTypes.string.isRequired,
	onChange: PropTypes.func.isRequired,
};
