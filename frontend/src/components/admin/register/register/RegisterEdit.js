import React from "react";
import { connect } from "react-redux";
import { createRegister, updateRegister } from "../../../actions/register/registers";
import Form from "../../forms/Form";
import { BoolField, SelectField, StringField } from "../../forms/fields";

class RegisterEdit extends React.Component {
	constructor(props) {
		super(props);
		this.state = this.getResetState();
	}

	componentWillMount() {
		this.reset();
	}

	getResetState(props = this.props) {
		if (props.register !== null)
			return { ...props.register };
		return {
			name: '',
			currency: '',
			is_cash_register: true,
			is_active: true,
			payment_type: 0,
		};
	}

	reset(evt, props) {
		if (evt)
			evt.preventDefault();
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
		if (this.props.register !== props.register)
			this.reset(null, props);
	}

	render() {
		const updateValue = key => evt => this.setState({ [key]: evt.target.value });

		return (
			<Form
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
			</Form>
		);
	}
}


export default connect(
	(state, props) => ({
		register: (state.registers.registers || []).filter(s => s.id === parseInt(props.params.registerID || '-1', 10))[0],
		currencies: state.currencies.currencies || [],
		paymentTypes: state.paymentTypes.paymentTypes || [],
	}),
	dispatch => ({
		addRegister: register => dispatch(createRegister(register)),
		editRegister: register => dispatch(updateRegister(register)),
	})
)(RegisterEdit);
