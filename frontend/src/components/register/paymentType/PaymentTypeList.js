import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import FontAwesome from '../../tools/icons/FontAwesome';
import { startFetchingPaymentTypes } from '../../../state/register/payment_types/actions.js';

class PaymentTypeList extends React.Component {
	constructor(props) {
		super(props);
		this.state = { open: true };
	}

	static RenderEntry({ paymentTypeID, register }) {
		return (
			<tr className={+paymentTypeID === register.id ? 'active' : null}>
				<td>
					{register.name}
				</td>
				<td>
					<div className="btn-group pull-right">
						{
							register.updating ? (
								<a
									className="btn btn-success btn-xs disabled"
									title="Updating">
									<FontAwesome icon="refresh" />
								</a>
							) : null
						}
						<Link
							to={`/register/paymenttype/${register.id}/`}
							className="btn btn-default btn-xs"
							title="Details">
							<FontAwesome icon="crosshairs" />
						</Link>
						<Link
							to={`/register/paymenttype/${register.id}/edit/`}
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
						List of payment types
					</h3>
					<div className="box-tools">
						<div className="input-group">
							<div className="btn-group">
								<a
									className={`btn btn-sm btn-default ${this.props.fetching ? 'disabled' : ''}`}
									title="Refresh"
									onClick={this.props.update}>
									<FontAwesome icon={`refresh ${this.props.fetching ? 'fa-spin' : ''}`} />
								</a>
								<Link
									className="btn btn-default btn-sm"
									to="/register/paymenttype/create/"
									title="Create new payment type">
									<FontAwesome icon="plus" />
								</Link>
							</div>
							<a className="btn btn-box-tool" onClick={::this.toggle} title={this.state.open ? 'Close box' : 'Open box'}>
								<FontAwesome icon={this.state.open ? 'minus' : 'plus'} />
							</a>
						</div>
					</div>
				</div>
				<div className="box-body">
					<table className="table table-striped">
						<thead>
							<tr>
								<th>
									<span>Payment type name</span>
								</th>
								<th>
									<span className="pull-right">Options</span>
								</th>
							</tr>
						</thead>
						<tbody>
							{(this.props.paymentTypes || []).map(
								item => (
									<PaymentTypeList.RenderEntry registerID={this.props.paymentTypeID} key={item.id} register={item} />
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

PaymentTypeList.propTypes = { paymentTypeID: PropTypes.string };

export default connect(
	state => ({
		errorMsg: state.register.registers.fetchError,
		paymentTypes: state.register.paymentTypes.paymentTypes,
		fetching: state.register.registers.fetching,
	}),
	{
		dispatch: evt => evt,
		update: startFetchingPaymentTypes,
	}
)(PaymentTypeList);
