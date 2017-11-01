import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Link } from 'react-router';
import FontAwesome from '../../tools/icons/FontAwesome';
import { fetchAllUnitTypes } from '../../../state/assortment/unit-types/actions.js';

class UnitTypeList extends React.Component {
	static propTypes = {
		toolButtons: PropTypes.oneOfType([
			PropTypes.element,
			PropTypes.arrayOf(PropTypes.element),
		]),
	};

	static RenderEntry({ activeID, unitType }) {
		return (
			<tr className={+activeID === unitType.id ? 'active' : null}>
				<td>
					{unitType.type_long}
				</td>
				<td>
					<div className="btn-group pull-right">
						<Link
							to={`/assortment/unittype/${unitType.id}/`}
							className="btn btn-default btn-xs"
							title="Details">
							<FontAwesome icon="crosshairs" />
						</Link>
						<Link
							to={`/assortment/unittype/${unitType.id}/edit/`}
							className="btn btn-default btn-xs"
							title="Edit">
							<FontAwesome icon="edit" />
						</Link>
					</div>
				</td>
			</tr>
		);
	}

	render() {
		return (
			<div className="box">
				<div className="box-header with-border">
					<h3 className="box-title">Unit types</h3>
					<div className="box-tools">
						<div className="input-group">
							<div className="btn-group">
								<Link
									className={`btn btn-sm ${this.props.invalid ? 'btn-danger' : 'btn-default'} ${this.props.fetching ? 'disabled' : ''}`}
									to="#"
									title="Refresh"
									onClick={this.props.update}>
									<FontAwesome icon={`refresh ${this.props.fetching ? 'fa-spin' : ''}`} />
								</Link>
								<Link
									className="btn btn-default btn-sm"
									to="/assortment/unittype/create/"
									title="Create new unit type">
									<FontAwesome icon="plus" />
								</Link>
							</div>
						</div>
					</div>
				</div>
				<div className="box-body">
					<table className="table table-striped">
						<thead>
							<tr>
								<th>
									<span>Label type name</span>
								</th>
								<th>
									<span className="pull-right">Options</span>
								</th>
							</tr>
						</thead>
						<tbody>
							{this.props.unitTypes === null ? null : this.props.unitTypes.map(
								unitType => (
									<UnitTypeList.RenderEntry activeID={this.props.activeID} key={unitType.id} unitType={unitType} />
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
		);
	}
}

export default connect(
	state => ({
		unitTypes: state.assortment.unitTypes.unitTypes,
		errorMsg: state.assortment.unitTypes.errorMsg,
		fetching: state.assortment.labelTypes.fetching,
	}),
	{
		update: fetchAllUnitTypes,
	},
)(UnitTypeList);
