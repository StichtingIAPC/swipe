import React from "react";
import { connect } from "react-redux";
import Form from "../../forms/Form";
import { StringField, IntegerField, SelectField } from "../../forms/fields";
import { updateAccountingGroup, createAccountingGroup } from "../../../actions/money/accountingGroups";

/**
 * Created by Matthias on 26/11/2016.
 */

class AccountingGroupEdit extends React.Component {
	constructor(props) {
		super(props);
		this.state = this.getResetState();
	}

	getResetState(props = this.props) {
		if (props.accountingGroup != null) return { ...props.accountingGroup };
		return { name: '', vat_group: '', accounting_number: '' }
	}

	reset() {
		this.setState(this.getResetState());
	}

	componentWillReceiveProps(props) {
		this.setState(this.getResetState(props));
	}

	save(evt) {
		evt.preventDefault();
		if (this.state.id) {
			this.props.updateAccountingGroup(this.state);
		} else {
			this.props.createAccountingGroup(this.state);
		}
	}

	render() {
		const accountingGroup = this.state;
		return (
			<Form
				title={this.props.currentID ? `Edit ${this.props.accountingGroup.name}` : 'Create new accounting group'}
				onReset={this.reset.bind(this)}
				onSubmit={this.save.bind(this)}
				error={this.props.errorMsg}
				returnLink={this.props.accountingGroup ? `/money/accountinggroup/${accountingGroup.id}/` : '/money/'}
				closeLink="/money/">
				<StringField name="Name" value={accountingGroup.name} onChange={evt => this.setState({name: evt.target.value})} />
				<IntegerField name="Accounting number" value={accountingGroup.accounting_number} onChange={evt => this.setState({accounting_number: Number(evt.target.value)})} />
				<SelectField name="VAT group" value={accountingGroup.vat_group} onChange={evt => this.setState({vat_group: evt.target.value})} selector="id" options={this.props.VATs} />
			</Form>
		)
	}
}

export default connect(
	(state, props) => ({
		errorMsg: state.currencies.inputError,
		accountingGroup: state.accountingGroups.accountingGroups.find(obj => Number(obj.id) == Number(props.params.accountingGroupID)),
		VATs: state.VATs.VATs || [],
	}),
	dispatch => ({
		updateAccountingGroup: (currency) => dispatch(updateAccountingGroup(currency)),
		createAccountingGroup: (currency) => dispatch(createAccountingGroup(currency)),
	}),
)(AccountingGroupEdit);
