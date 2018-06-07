import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { fetchAllCurrencies } from '../../../state/money/currencies/actions.js';
import FontAwesome from '../../tools/icons/FontAwesome';
import { Box } from 'reactjs-admin-lte';

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
								<a
									className="btn btn-success btn-xs disabled"
									title="Updating">
									<FontAwesome icon="refresh" />
								</a>
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

	toggle = evt => {
		evt.preventDefault();
		this.setState(({ open }) => ({ open: !open }));
	};

	update = evt => {
		evt.preventDefault();
		this.props.fetchAllCurrencies();
	};

	render() {
		return (
			<Box
				closable={true}
				error={!!this.props.errorMsg}
				header={{
					title: 'List of currencies',
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
								to="/money/currency/create/"
								title="Create new currency">
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
			</Box>
		);
	}
}

export default connect(
	state => ({
		errorMsg: state.money.currencies.fetchError,
		currencies: state.money.currencies.currencies,
		fetching: state.money.currencies.fetching,
	}),
	{
		fetchAllCurrencies,
	}
)(CurrencyList);
