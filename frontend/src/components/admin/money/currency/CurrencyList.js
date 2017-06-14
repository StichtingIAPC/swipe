import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router';
import { connect } from 'react-redux';
import { startFetchingCurrencies } from '../../../../actions/money/currencies';
import FontAwesome from '../../../tools/icons/FontAwesome';
/**
 * Created by Matthias on 26/11/2016.
 */

class CurrencyList extends React.Component {
	static propTypes = {
		activeID: PropTypes.string,
	};

	constructor(props) {
		super(props);
		this.state = { open: true };
	}

	static RenderEntry({ activeID, currency }) {
		return (
			<tr className={activeID === currency.iso ? 'active' : null}>
				<td>
					{`${currency.name} (${currency.iso})`}
				</td>
				<td>
					<div className="btn-group pull-right">
						{
							currency.updating ? (
								<Link
									className="btn btn-success btn-xs disabled"
									title="Updating">
									<FontAwesome icon="refresh" />
								</Link>
							) : null
						}
						<Link
							to={`/money/currency/${currency.iso}/`}
							className="btn btn-default btn-xs"
							title="Details">
							<FontAwesome icon="crosshairs" />
						</Link>
						<Link
							to={`/money/currency/${currency.iso}/edit/`}
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
						List of currencies
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
							<Link className="btn btn-sm btn-box-tool" onClick={::this.toggle} title={this.state.open ? 'Close box' : 'Open box'}>
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
									<span>Currency name</span>
								</th>
								<th>
									<span className="pull-right">Options</span>
								</th>
							</tr>
						</thead>
						<tbody>
							{
								this.props.currencies === null ? null : this.props.currencies.map(
									item => (
										<CurrencyList.RenderEntry activeID={this.props.activeID} key={item.iso} currency={item} />
									)
								)
							}
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
		errorMsg: state.currencies.fetchError,
		currencies: state.currencies.currencies || [],
		fetching: state.currencies.fetching,
	}),
	dispatch => ({
		update: evt => {
			evt.preventDefault();
			dispatch(startFetchingCurrencies());
		},
	})
)(CurrencyList);
