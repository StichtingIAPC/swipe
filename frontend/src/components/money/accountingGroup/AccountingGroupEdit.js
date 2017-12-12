import React from 'react';
import { connect } from 'react-redux';
import Form from '../../forms/Form';
import { IntegerField, SelectField, StringField } from '../../forms/fields';
import { createAccountingGroup, updateAccountingGroup } from '../../../state/money/accounting-groups/actions.js';

/**
 * Created by Matthias on 26/11/2016.
 */

class AccountingGroupEdit extends React.Component {
	constructor(props) {
		super(props);
		this.state = this.getResetState();
	}

	getResetState(props = this.props) {
		if (props.accountingGroup !== null) {
			return { ...props.accountingGroup };
		}
		return {
			name: '',
			vat_group: '',
			accounting_number: '',
		};
	}

	reset() {
		this.setState(this.getResetState());
	}

	componentWillReceiveProps(props) {
		this.setState(this.getResetState(props));
	}

	save(evt) {
		evt.preventDefault();
		if (this.props.accountingGroup) {
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
				onReset={::this.reset}
				onSubmit={::this.save}
				error={this.props.errorMsg}
				returnLink={this.props.accountingGroup ? `/money/accountinggroup/${accountingGroup.id}/` : '/money/'}
				closeLink="/money/">
				<StringField
					name="Name" value={accountingGroup.name}
					onChange={evt => this.setState({ name: evt.target.value })} />
				<IntegerField
					name="Accounting number" value={accountingGroup.accounting_number}
					onChange={evt => this.setState({ accounting_number: Number(evt.target.value) })} />
				<SelectField
					name="VAT group" value={accountingGroup.vat_group}
					onChange={evt => this.setState({ vat_group: evt.target.value })} selector="id"
					options={this.props.VATs} />
			</Form>
		);
	}
}

export default connect(
	state => ({
		errorMsg: state.money.currencies.inputError,
		accountingGroup: state.money.accountingGroups.activeObject,
		vats: state.money.vats.vats || [],
	}),
	{
		updateAccountingGroup,
		createAccountingGroup,
	},
)(AccountingGroupEdit);
