import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import FontAwesome from '../../tools/icons/FontAwesome';

/**
 * Created by Matthias on 26/11/2016.
 */

class CurrencyDetail extends React.Component {
	trash(evt) {
		evt.preventDefault();
	}

	render() {
		const { currency } = this.props;

		if (!currency) {
			return null;
		}

		return (
			<div className="box">
				<div className="box-header with-border">
					<h3 className="box-title">Currency: {currency.name}</h3>
					<div className="box-tools">
						<div className="input-group">
							<div className="btn-group">
								<Link to={`/money/currency/${currency.iso}/edit/`} className="btn btn-default btn-sm" title="Edit"><FontAwesome icon="edit" /></Link>
								<Link onClick={::this.trash} className="btn btn-danger btn-sm" title="Delete"><FontAwesome icon="trash" /></Link>
							</div>
						</div>
					</div>
				</div>
				<div className="box-body">
					<dl className="dl-horizontal">
						{Object.entries({
							iso: 'ISO',
							name: 'Name',
							digits: 'Digits',
							symbol: 'Symbol',
						}).map(
							([ key, name ]) => (
								<div key={key}>
									<dt>{name}</dt>
									<dd>{String(currency[key])}</dd>
								</div>
							)
						)}
						<div>
							<dt>Available denominations</dt>
							<dd>
								{currency.denomination_set.length > 0 ? currency.denomination_set.map(
									denom => {
										const { amount } = denom;

										return (
											<span key={amount} className="label label-denomination">
												{currency.symbol} {amount.substr(0, amount.indexOf('.') + currency.digits + (currency.digits > 0))}
											</span>
										);
									}
								) : 'none'}
							</dd>
						</div>
					</dl>
				</div>
			</div>
		);
	}
}

export default connect(
	(state, ownProps) => ({ currency: state.money.currencies.currencies.find(obj => obj.iso === ownProps.params.currencyID) })
)(CurrencyDetail);
