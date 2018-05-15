import React from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import Select from 'react-select';

class CustomerSelector extends React.Component {
	componentWillMount() {
	}

	render() {
		const customerList = this.props.customers.map(customer => ({ value: customer.id, label: customer.name }));

		return (
			<div className="row">

				<Select
					name="form-field-name"
					value={1}
					onChange={obj => this.props.onChange(obj.value)}
					options={customerList} />
				<br />

			</div>
		);
	}
}

CustomerSelector.proptypes = {
	onChange: PropTypes.func.isRequired,
	customer: PropTypes.number.isRequired,
};

export default connect(
	state => ({
		customers: state.crm,
	}),
)(CustomerSelector);
