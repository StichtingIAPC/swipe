import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import FontAwesome from '../../tools/icons/FontAwesome';
import { fetchAllAccountingGroups } from '../../../state/money/accounting-groups/actions.js';
import { Box } from 'reactjs-admin-lte';

class AccountingGroupList extends React.Component {
	constructor(props) {
		super(props);
		this.state = { open: true };
	}

	static RenderEntry({ activeID, accountingGroup }) {
		return (
			<tr className={activeID === accountingGroup.id ? 'active' : null}>
				<td>
					{accountingGroup.name}
				</td>
				<td>
					<div className="btn-group pull-right">
						{
							accountingGroup.updating ? (
								<a
									className="btn btn-success btn-xs disabled"
									title="Updating">
									<FontAwesome icon="refresh" />
								</a>
							) : null
						}
						<Link
							to={`/money/accountinggroup/${accountingGroup.id}/`}
							className="btn btn-default btn-xs"
							title="Details">
							<FontAwesome icon="crosshairs" />
						</Link>
						<Link
							to={`/money/accountinggroup/${accountingGroup.id}/edit/`}
							className="btn btn-default btn-xs"
							title="Edit">
							<FontAwesome icon="edit" />
						</Link>
					</div>
				</td>
			</tr>
		);
	}

	toggle = evt => {
		evt.preventDefault();
		this.setState({ open: !this.state.open });
	};

	update = evt => {
		evt.preventDefault();
		this.props.fetchAllAccountingGroups();
	};

	render() {
		return (
			<Box
				closable={true}
				error={!!this.props.errorMsg}
				header={{
					title: 'List of accounting groups',
					buttons: (
						<React.Fragment>
							<a
								className={`btn btn-sm btn-default ${this.props.fetching ? 'disabled' : ''}`}
								title="Refresh"
								onClick={this.update}>
								<FontAwesome icon={`refresh ${this.props.fetching ? 'fa-spin' : ''}`} />
							</a>
							<Link
								className="btn btn-sm btn-default"
								to="/money/accountinggroup/create/"
								title="Create new accounting group">
								<FontAwesome icon="plus" />
							</Link>
						</React.Fragment>
					),
				}}>
				<Box.Body>
					<table className="table table-striped">
						<thead>
							<tr>
								<th>
									<span>Accounting group name</span>
								</th>
								<th>
									<span className="pull-right">Options</span>
								</th>
							</tr>
						</thead>
						<tbody>
							{this.props.accountingGroups.map(
								item => (
									<AccountingGroupList.RenderEntry activeID={this.props.activeID} key={item.id} accountingGroup={item} />
								)
							)}
						</tbody>
					</table>
				</Box.Body>
				{
					this.props.errorMsg ? (
						<Box.Footer>
							<FontAwesome icon="warning" />
							<span>{this.props.errorMsg}</span>
						</Box.Footer>
					) : null
				}
			</Box>
		);
	}
}

AccountingGroupList.propTypes = { activeID: PropTypes.string };

export default connect(
	state => ({
		errorMsg: state.money.accountingGroups.fetchError,
		accountingGroups: state.money.accountingGroups.accountingGroups || [],
		fetching: state.money.accountingGroups.fetching,
	}),
	{
		fetchAllAccountingGroups,
	}
)(AccountingGroupList);
