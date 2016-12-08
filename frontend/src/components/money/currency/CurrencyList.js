import React, {PropTypes} from "react";
import {Link} from "react-router";
import {connect} from "react-redux";
import {populateCurrencies} from "../../../actions/money/currencies";
import FontAwesome from "../../tools/icons/FontAwesome";
/**
 * Created by Matthias on 26/11/2016.
 */

class CurrencyList extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			open: true,
		}
	}

	renderEntry({activeID, currency}) {
		return (
			<tr className={Number(activeID) == currency.iso ? 'active' : null}>
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
		)
	}

	toggle(evt) {
		evt.preventDefault();
		this.setState({open: !this.state.open});
	}

	render() {
		return (
			<div className={`box ${this.props.invalid ? 'box-danger' : 'box-success'} ${this.state.open ? '' : 'collapsed-box'}`}>
				<div className="box-header with-border">
					<h3 className="box-title">List of currencies</h3>
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
									to="/money/currency/create/"
									title="Create new currency">
									<FontAwesome icon="plus" />
								</Link>
							</div>
							<Link className="btn btn-box-tool" onClick={this.toggle.bind(this)} title={this.state.open ? 'Close box' : 'Open box'}>
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
							{Object.keys(this.props.currencies).filter(key => this.props.currencies[key]).map(
								(id) => (
									<this.renderEntry activeID={this.props.currencyID} key={id} currency={this.props.currencies[id]} />
								)
							)}
						</tbody>
					</table>
				</div>
			</div>
		)
	}
}

CurrencyList.propTypes = {
	activeID: PropTypes.string,
};

export default connect(
	(state, ownProps) => ({
		...ownProps,
		currencies: state.currencies.objects,
		invalid: state.currencies.invalid,
		fetching: state.currencies.fetching,
	}),
	(dispatch, ownProps) => ({
		...ownProps,
		update: (evt) => {
			evt.preventDefault();
			dispatch(populateCurrencies());
		},
	})
)(CurrencyList);
