import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Link } from 'react-router';
import FontAwesome from '../../tools/icons/FontAwesome';
import { startFetchingLabelTypes } from '../../../actions/assortment/labelTypes';

class LabelTypeList extends React.Component {
	static propTypes = {
		toolButtons: PropTypes.oneOfType([
			PropTypes.element,
			PropTypes.arrayOf(PropTypes.element),
		]),
	};

	static RenderEntry({ activeID, labelType }) {
		return (
			<tr className={+activeID === labelType.id ? 'active' : null}>
				<td>
					{labelType.name}
				</td>
				<td>
					<div className="btn-group pull-right">
						<Link
							to={`/assortment/labeltype/${labelType.id}/`}
							className="btn btn-default btn-xs"
							title="Details">
							<FontAwesome icon="crosshairs" />
						</Link>
						<Link
							to={`/assortment/labeltype/${labelType.id}/edit/`}
							className="btn btn-default btn-xs"
							title="Edit">
							<FontAwesome icon="edit" />
						</Link>
					</div>
				</td>
			</tr>
		);
	}

	update(evt) {
		evt.preventDefault();
		this.props.update();
	}

	render() {
		return (
			<div className="box">
				<div className="box-header with-border">
					<h3 className="box-title">Label types</h3>
					<div className="box-tools">
						<div className="input-group">
							<div className="btn-group">
								<Link
									className={`btn btn-sm ${this.props.invalid ? 'btn-danger' : 'btn-default'} ${this.props.fetching ? 'disabled' : ''}`}
									to="#"
									title="Refresh"
									onClick={::this.update}>
									<FontAwesome icon={`refresh ${this.props.fetching ? 'fa-spin' : ''}`} />
								</Link>
								<Link
									className="btn btn-default btn-sm"
									to="/assortment/labeltype/create/"
									title="Create new label type">
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
							{this.props.labelTypes === null ? null : this.props.labelTypes.map(
								labelType => (
									<LabelTypeList.RenderEntry activeID={this.props.activeID} key={labelType.id} labelType={labelType} />
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
		labelTypes: state.labelTypes.labelTypes,
		errorMsg: state.labelTypes.errorMsg,
		fetching: state.labelTypes.fetching,
	}),
	dispatch => ({ update: () => dispatch(startFetchingLabelTypes()) }),
)(LabelTypeList);
