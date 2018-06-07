import React from 'react';
import { connect } from 'react-redux';
import Card from '../../base/Card';
import { IntegerField, SelectField, StringField } from '../../forms/fields';
import { createAccountingGroup, updateAccountingGroup, resetAccountingGroup, fetchAccountingGroup } from '../../../state/money/accounting-groups/actions.js';
import { setAccountingGroupField } from '../../../state/money/accounting-groups/actions';

/**
 * Created by Matthias on 26/11/2016.
 */

class AccountingGroupEdit extends React.Component {
	componentWillMount() {
		const { match: { params: { accountingGroupId }}} = this.props;

		if (typeof accountingGroupId === 'undefined') {
			this.props.resetAccountingGroup();
		} else {
			this.props.fetchAccountingGroup(accountingGroupId);
		}
	}

	componentWillReceiveProps({ match: { params: { accountingGroupId }}}) {
		if (accountingGroupId !== this.props.match.params.accountingGroupId) {
			if (typeof accountingGroupId === 'undefined') {
				this.props.resetAccountingGroup();
			} else {
				this.props.fetchAccountingGroup(accountingGroupId);
			}
		}
	}

	reset = () => {
		const { match } = this.props;

		if (typeof match.params.accountingGroupId === 'undefined') {
			this.props.resetAccountingGroup();
		} else {
			this.props.fetchAccountingGroup(match.params.accountingGroupId);
		}
	};

	save = () => {
		const { accountingGroup } = this.props;

		if (accountingGroup.id === null) {
			this.props.createAccountingGroup(accountingGroup);
		} else {
			this.props.updateAccountingGroup(accountingGroup);
		}
	};

	setName = ({ target: { value }}) => this.props.setAccountingGroupField('name', value);
	setAccountingNumber = ({ target: { value }}) => this.props.setAccountingGroupField('accounting_number', value);
	setVatGroup = ({ target: { value }}) => this.props.setAccountingGroupField('vat_group', value);

	render() {
		const { accountingGroup } = this.props;

		return (
			<Card
				title={this.props.accountingGroup.id === null ? 'Create new accounting group' : `Edit ${this.props.accountingGroup.name}`}
				onReset={this.reset}
				onSubmit={this.save}
				error={this.props.errorMsg}
				returnLink={this.props.accountingGroup.id === null ? '/money/' : `/money/accountinggroup/${accountingGroup.id}/`}
				closeLink="/money/">
				<StringField
					name="Name" value={accountingGroup.name}
					onChange={this.setName} />
				<IntegerField
					name="Accounting number" value={accountingGroup.accounting_number}
					onChange={this.setAccountingNumber} />
				<SelectField
					name="VAT group" value={accountingGroup.vat_group}
					onChange={this.setVatGroup} selector="id"
					options={this.props.vats} />
			</Card>
		);
	}
}

export default connect(
	state => ({
		errorMsg: state.money.currencies.inputError,
		accountingGroup: state.money.accountingGroups.activeObject,
		vats: state.money.vats.vats,
	}),
	{
		updateAccountingGroup,
		createAccountingGroup,
		resetAccountingGroup,
		fetchAccountingGroup,
		setAccountingGroupField,
	},
)(AccountingGroupEdit);
