import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import FontAwesome from '../../tools/icons/FontAwesome';

/**
 * Created by Matthias on 26/11/2016.
 */

class AccountingGroupDetail extends React.Component {
	trash = evt => evt.preventDefault();

	render() {
		const { accountingGroup } = this.props;

		if (!accountingGroup) {
			return null;
		}

		return (
			<div className="box">
				<div className="box-header with-border">
					<h3 className="box-title">Accounting group: {accountingGroup.name}</h3>
					<div className="box-tools">
						<div className="input-group">
							<div className="btn-group">
								<Link to={`/money/accountinggroup/${accountingGroup.id}/edit/`} className="btn btn-default btn-sm" title="Edit"><FontAwesome icon="edit" /></Link>
								<a onClick={this.trash} className="btn btn-danger btn-sm" title="Delete"><FontAwesome icon="trash" /></a>
							</div>
						</div>
					</div>
				</div>
				<div className="box-body">
					<dl className="dl-horizontal">
						{Object.entries({
							name: 'Name',
							accounting_number: 'Accounting number',
						}).map(
							([ key, name ]) => (
								<React.Fragment key={key}>
									<dt>{name}</dt>
									<dd>{String(accountingGroup[key])}</dd>
								</React.Fragment>
							)
						)}
						<dt>VAT group</dt>
						<dd>{(this.props.vat || {}).name}</dd>
					</dl>
				</div>
			</div>
		);
	}
}

export default connect(
	state => {
		const accountingGroup = state.money.accountingGroups.activeObject;

		return {
			accountingGroup,
			vat: (state.money.vats.vats || []).find(el => +el.id === +accountingGroup.vat_group),
		};
	}
)(AccountingGroupDetail);
