import React from 'react';
import { connect } from 'react-redux';
import { createPaymentType, updatePaymentType } from '../../../../state/register/payment-types/actions.js';
import Form from '../../../forms/Form';
import { BoolField, StringField } from '../../../forms/fields';

class PaymentTypeEdit extends React.Component {
	constructor(props) {
		super(props);
		this.state = this.getResetState();
	}

	componentWillMount() {
		this.reset();
	}

	getResetState(props = this.props) {
		if (props.paymentType !== null) {
			return { ...props.paymentType };
		}
		return {
			name: '',
			is_invoicing: false,
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
			this.props.addPaymentType({
				...this.state,
				lastModified: new Date(),
			});
		} else {
			this.props.editPaymentType({
				...this.state,
				lastModified: new Date(),
			});
		}
	}

	componentWillReceiveProps(props) {
		if (this.props.paymentType !== props.paymentType) {
			this.reset(null, props);
		}
	}

	render() {
		return (
			<Form
				title={`${this.state.id ? 'Edit' : 'Add'} payment type`}
				onSubmit={::this.submit}
				onReset={::this.reset}
				error={this.props.errorMsg}
				returnLink={this.props.paymentType ? `/register/paymenttype/${this.props.paymentType.id}/` : '/paymentType/'}
				closeLink="/register/">
				<StringField name="Name" value={this.state.name} onChange={evt => this.setState({ name: evt.target.value })} />
				<BoolField name="Is invoicing" value={this.state.is_invoicing} onChange={() => this.setState(({ is_invoicing }) => ({ is_invoicing: !is_invoicing }))} />
				{/* <SelectField
					onChange={updateValue('payment_type')}
					name="Payment type"
					value={this.state.payment_type}
					options={this.state.payment_types} />*/}
			</Form>
		);
	}
}


export default connect(
	(state, props) => ({
		// TODO: replace with fetcher
		paymentType: state.register.paymentTypes.paymentTypes.filter(s => s.id === +props.params.paymentTypeID)[0],
	}),
	{
		addPaymentType: createPaymentType,
		editPaymentType: updatePaymentType,
	}
)(PaymentTypeEdit);
