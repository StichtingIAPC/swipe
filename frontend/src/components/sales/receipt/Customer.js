import React from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import Select from 'react-select';
import { getCustomerList } from '../../../state/crm/selectors';
import { newAction as newExternalise } from '../../../state/logistics/externalise/actions';
import { fetchCustomersAction } from '../../../state/crm/actions';

class CustomerSelector extends React.Component {
	componentWillMount() {
		this.props.fetchCustomersAction();
	}

	getCustomerName(customer) {
		return `${customer.person.name || ''} ${(customer.organisation || { name: '' }).name}`;
	}
	render() {
		const customerList = this.props.customers.map(customer => ({ value: customer.person.id,
			label: this.getCustomerName(customer) }));

		return (
			<div className="row">
				<div className="col-md-6 form-group">
					<label htmlFor={this.props.id}>Customer</label>
					<Select
						id={this.props.id}
						value={this.props.customer}
						onChange={obj => { console.log(obj); this.props.onChange(obj ? obj.value : null); }}
						options={customerList} />
					<br />
				</div>
			</div>
		);
	}
}

CustomerSelector.proptypes = {
	onChange: PropTypes.func.isRequired,
	customer: PropTypes.number.isRequired,
	id: PropTypes.string.isRequired,
};

export default connect(
	state => ({
		customers: getCustomerList(state),
	}),
	{
		fetchCustomersAction,
	},
)(CustomerSelector);
