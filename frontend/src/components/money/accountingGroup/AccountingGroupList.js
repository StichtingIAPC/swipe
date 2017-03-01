import React, { PropTypes } from "react";
import { connect } from "react-redux";
import { Link } from "react-router";
import FontAwesome from "../../tools/icons/FontAwesome";
import { startFetchingAccountingGroups } from "../../../actions/money/accountingGroups";

class AccountingGroupList extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			open: true,
		}
	}

	renderEntry({activeID, accountingGroup}) {
		return (
			<tr className={activeID == accountingGroup.id ? 'active' : null}>
				<td>
					{accountingGroup.name}
				</td>
				<td>
					<div className="btn-group pull-right">
						{
							accountingGroup.updating ? (
								<Link
									className="btn btn-success btn-xs disabled"
									title="Updating">
									<FontAwesome icon="refresh" />
								</Link>
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
		)
	}

	toggle(evt) {
		evt.preventDefault();
		this.setState({open: !this.state.open});
	}

	render() {
		return (
			<div
				className={
					`box${
						this.state.open ? '' : ' collapsed-box'
					}${
						this.props.errorMsg ? ' box-danger box-solid' : ''
					}`
				}>
				<div className="box-header with-border">
					<h3 className="box-title">
						List of accounting groups
					</h3>
					<div className="box-tools">
						<div className="input-group">
							<div className="btn-group">
								<Link
									className={`btn btn-sm btn-default ${this.props.fetching ? 'disabled' : ''}`}
									title="Refresh"
									onClick={this.props.update}>
									<FontAwesome icon={`refresh ${this.props.fetching ? 'fa-spin' : ''}`} />
								</Link>
								<Link
									className="btn btn-sm btn-default"
									to="/money/currency/create/"
									title="Create new currency">
									<FontAwesome icon="plus" />
								</Link>
							</div>
							<Link className="btn btn-sm btn-box-tool" onClick={this.toggle.bind(this)} title={this.state.open ? 'Close box' : 'Open box'}>
								<FontAwesome icon={this.state.open ? 'minus' : 'plus'} />
							</Link>
						</div>
					</div>
				</div>
				<div className="box-body">
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
								(item) => (
									<this.renderEntry activeID={this.props.activeID} key={item.id} accountingGroup={item} />
								)
							)}
						</tbody>
					</table>
				</div>
				{
					this.props.errorMsg ? (
						<div className="box-footer">
							<FontAwesome icon="warning" />
							<span>{this.props.errorMsg}</span>
						</div>
					) : null
				}
			</div>
		)
	}
}

AccountingGroupList.propTypes = {
	activeID: PropTypes.string,
};

export default connect(
	state => ({
		errorMsg: state.accountingGroups.fetchError,
		accountingGroups: state.accountingGroups.accountingGroups || [],
		fetching: state.accountingGroups.fetching,
	}),
	(dispatch) => ({
		update: (evt) => {
			evt.preventDefault();
			dispatch(startFetchingAccountingGroups());
		},
	})
)(AccountingGroupList);
