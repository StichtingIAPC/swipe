import React from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import Select from 'react-select';

class CustomerSelector extends React.Component {
	componentWillMount () {
	}

	render () {
		const customerList = this.props.customers.map (customer => ({ value: customer.id, label: customer.name }));

		return (
			<div className="row">
				<div className="col-md-6 form-group">
					<label htmlFor="custSelect">Customer</label>
					<Select
						id="custSelect"
						name="form-field-name"
						value={this.props.customer}
						onChange={obj => this.props.onChange(obj ? obj.value : null)}
						options={customerList}/>
					<br/>
				</div>


			</div>
		);
	}
}

CustomerSelector.proptypes = {
	onChange: PropTypes.func.isRequired,
	customer: PropTypes.number.isRequired,
};

export default connect (
	state => ({
		customers: state.crm,
	}),
) (CustomerSelector);
