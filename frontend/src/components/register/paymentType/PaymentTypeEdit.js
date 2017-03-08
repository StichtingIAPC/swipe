import React from "react";
import { connect } from "react-redux";
import { createPaymentType, updatePaymentType } from "../../../actions/register/paymentTypes";
import Form from "../../forms/Form";
import { StringField, BoolField } from "../../forms/fields";

class PaymentTypeEdit extends React.Component {
	constructor(props) {
		super(props);
		this.state = this.getResetState();
	}

	componentWillMount() {
		this.reset();
	}

	getResetState(props = this.props) {
		if (props.paymentType != null) return { ...props.paymentType };
		return { name: '', is_invoicing: false };
	}

	reset(evt, props) {
		if (evt) evt.preventDefault();
		this.setState(this.getResetState(props));
	}

	submit(evt) {
		evt.preventDefault();
		if (this.state.id == null) {
			this.props.addPaymentType({ ...this.state, lastModified: new Date() });
		} else {
			this.props.editPaymentType({ ...this.state, lastModified: new Date() });
		}
	}

	componentWillReceiveProps(props) {
		if (this.props.paymentType != props.paymentType) this.reset(undefined, props);
	}

	render() {
		const updateValue = key => evt => this.setState({ [key]: evt.target.value });

		return (
			<Form
				title={(!!this.state.id ? 'Edit' : 'Add') + " payment type"}
				onSubmit={this.submit.bind(this)}
				onReset={this.reset.bind(this)}
				error={this.props.errorMsg}
				returnLink={this.props.paymentType ? `/register/paymenttype/${this.props.paymentType.id}/` : '/paymentType/'}
				closeLink="/register/">
				<StringField name="Name" value={this.state.name} onChange={evt => this.setState({name: evt.target.value})} />
				<BoolField name="Is invoicing" value={this.state.is_invoicing} onChange={evt => this.setState(({is_invoicing}) => ({is_invoicing: !is_invoicing}))} />
				{/*<SelectField
					onChange={updateValue('payment_type')}
					name="Payment type"
					value={this.state.payment_type}
					options={this.state.payment_types} />*/}
			</Form>
		)
	}
}


export default connect(
	(state, props) => ({
		paymentType: (state.paymentTypes.paymentTypes || []).filter(s => s.id === parseInt(props.params.paymentTypeID || '-1'))[0],
	}),
	dispatch => ({
		addPaymentType: paymentType => dispatch(createPaymentType(paymentType)),
		editPaymentType: paymentType => dispatch(updatePaymentType(paymentType)),
	})
)(PaymentTypeEdit);
