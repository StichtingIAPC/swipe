import React from 'react';
import { connect } from 'react-redux';
import { createRegister, updateRegister } from '../../../state/register/registers/actions.js';
import Card from '../../base/Card';
import { BoolField, SelectField, StringField } from '../../forms/fields';

class RegisterEdit extends React.Component {
	constructor(props) {
		super(props);
		this.state = this.getResetState();
	}

	componentWillMount() {
		this.reset();
	}

	getResetState(props = this.props) {
		if (props.register !== null) {
			return { ...props.register };
		}
		return {
			name: '',
			currency: '',
			is_cash_register: true,
			is_active: true,
			payment_type: 0,
		};
	}

	reset(evt, props) {
		if (evt) {
			evt.preventDefault();
		}
		this.setState(this.getResetState(props));
	}

	submit(evt) {
		evt.preventDefault();
		if (this.state.id === null) {
			this.props.addRegister({
				...this.state,
				lastModified: new Date(),
			});
		} else {
			this.props.editRegister({
				...this.state,
				lastModified: new Date(),
			});
		}
	}

	componentWillReceiveProps(props) {
		if (this.props.register !== props.register) {
			this.reset(null, props);
		}
	}

	render() {
		const updateValue = key => evt => this.setState({ [key]: evt.target.value });

		return (
			<Card
				title={`${this.state.id ? 'Edit' : 'Add'} register`}
				onSubmit={::this.submit}
				onReset={::this.reset}
				error={this.props.errorMsg}
				returnLink={this.props.register ? `/register/register/${this.props.register.id}/` : '/register/'}
				closeLink="/register/">
				<StringField
					onChange={updateValue('name')}
					value={this.state.name}
					name="Name" />
				<SelectField
					onChange={updateValue('currency')}
					value={this.state.currency}
					selector="iso"
					name="Currency"
					options={this.props.currencies} />
				<BoolField
					onChange={() => this.setState(({ is_cash_register }) => ({ is_cash_register: !is_cash_register }))}
					value={this.state.is_cash_register}
					name="Cash register" />
				<BoolField
					onChange={() => this.setState(({ is_active }) => ({ is_active: !is_active }))}
					name="Active"
					value={this.state.is_active} />
				<SelectField
					onChange={updateValue('payment_type')}
					name="Payment type"
					value={this.state.payment_type}
					options={this.props.paymentTypes} />
			</Card>
		);
	}
}


export default connect(
	(state, props) => ({
		// TODO: replace with fetch
		register: state.register.registers.registers.filter(s => s.id === +props.params.registerID)[0],
		currencies: state.money.currencies.currencies,
		paymentTypes: state.register.paymentTypes.paymentTypes,
	}),
	{
		addRegister: createRegister,
		editRegister: updateRegister,
	}
)(RegisterEdit);
