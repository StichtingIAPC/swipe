import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Link } from 'react-router';
import FontAwesome from '../../tools/icons/FontAwesome';
import { startFetchingRegisters } from '../../../actions/register/registers';

class RegisterList extends React.Component {
	static propTypes = {
		registerID: PropTypes.string,
	};

	constructor(props) {
		super(props);
		this.state = { open: true };
	}

	static RenderEntry({ registerID, register }) {
		return (
			<tr className={+registerID === register.id ? 'active' : null}>
				<td>
					{register.name}
				</td>
				<td>
					<div className="btn-group pull-right">
						{
							register.updating ? (
								<Link
									className="btn btn-success btn-xs disabled"
									title="Updating">
									<FontAwesome icon="refresh" />
								</Link>
							) : null
						}
						<Link
							to={`/register/register/${register.id}/`}
							className="btn btn-default btn-xs"
							title="Details">
							<FontAwesome icon="crosshairs" />
						</Link>
						<Link
							to={`/register/register/${register.id}/edit/`}
							className="btn btn-default btn-xs"
							title="Edit">
							<FontAwesome icon="edit" />
						</Link>
					</div>
				</td>
			</tr>
		);
	}

	toggle(evt) {
		evt.preventDefault();
		this.setState({ open: !this.state.open });
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
						List of registers
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
									className="btn btn-default btn-sm"
									to="/register/register/create/"
									title="Create new register">
									<FontAwesome icon="plus" />
								</Link>
							</div>
							<Link className="btn btn-box-tool" onClick={::this.toggle} title={this.state.open ? 'Close box' : 'Open box'}>
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
									<span>Register name</span>
								</th>
								<th>
									<span className="pull-right">Options</span>
								</th>
							</tr>
						</thead>
						<tbody>
							{this.props.registers.map(
								item => (
									<RegisterList.RenderEntry registerID={this.props.registerID} key={item.id} register={item} />
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
		errorMsg: state.registers.fetchError,
		registers: state.registers.registers || [],
		fetching: state.registers.fetching,
	}),
	dispatch => ({
		dispatch,
		update: evt => {
			evt.preventDefault();
			dispatch(startFetchingRegisters());
		},
	}),
)(RegisterList);
