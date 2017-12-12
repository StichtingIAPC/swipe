import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import FontAwesome from '../../tools/icons/FontAwesome';
import { fetchAllvats } from '../../../state/money/vats/actions.js';
import Box from '../../base/Box';

class VATList extends React.Component {
	static propTypes = {
		activeID: PropTypes.string,
	};

	constructor(props) {
		super(props);
		this.state = { open: true };
	}

	static RenderEntry({ activeID, vat }) {
		return (
			<tr className={+activeID === vat.id ? 'active' : null}>
				<td>
					{vat.name}
				</td>
				<td>
					<div className="btn-group pull-right">
						{
							vat.updating ? (
								<a
									className="btn btn-success btn-xs disabled"
									title="Updating">
									<FontAwesome icon="refresh" />
								</a>
							) : null
						}
						<Link
							to={`/money/vat/${vat.id}/`}
							className="btn btn-default btn-xs"
							title="Details">
							<FontAwesome icon="crosshairs" />
						</Link>
						<Link
							to={`/money/vat/${vat.id}/edit/`}
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

	render() {
		return (
			<Box
				closable={true}
				error={!!this.props.errorMsg}
				header={{
					title: 'List of VATs',
					buttons: (
						<React.Fragment>
							<a
								className={`btn btn-sm btn-default ${this.props.fetching ? 'disabled' : ''}`}
								title="Refresh"
								onClick={this.props.update}>
								<FontAwesome icon={`refresh ${this.props.fetching ? 'fa-spin' : ''}`} />
							</a>
							<Link
								className="btn btn-default btn-sm"
								to="/money/vat/create/"
								title="Create new VAT">
								<FontAwesome icon="plus" />
							</Link>
						</React.Fragment>
					),
				}}>
				<div className="box-body">
					<table className="table table-striped">
						<thead>
							<tr>
								<th>
									<span>VAT name</span>
								</th>
								<th>
									<span className="pull-right">Options</span>
								</th>
							</tr>
						</thead>
						<tbody>
							{this.props.vats.map(
								item => (
									<VATList.RenderEntry activeID={this.props.VATID} key={item.id} vat={item} />
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
			</Box>
		);
	}
}

export default connect(
	state => ({
		errorMsg: state.money.vats.error,
		vats: state.money.vats.vats,
		fetching: state.money.vats.fetching,
	}),
	{
		update: () => fetchAllvats(),
	}
)(VATList);
