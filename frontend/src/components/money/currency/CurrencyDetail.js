import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import FontAwesome from '../../tools/icons/FontAwesome';
import Box from '../../base/Box';

/**
 * Created by Matthias on 26/11/2016.
 */

class CurrencyDetail extends React.Component {
	trash = evt => evt.preventDefault();

	render() {
		const { currency } = this.props;

		if (!currency) {
			return null;
		}

		return (
			<Box className="box">
				<Box.Header
					title={`Currency: ${currency.name}`}
					buttons={
						<React.Fragment>
							<Link to={`/money/currency/${currency.iso}/edit/`} className="btn btn-default btn-sm" title="Edit"><FontAwesome icon="edit" /></Link>
							<a onClick={this.trash} className="btn btn-danger btn-sm" title="Delete"><FontAwesome icon="trash" /></a>
						</React.Fragment>
					} />
				<Box.Body>
					<dl className="dl-horizontal">
						{Object.entries({
							iso: 'ISO',
							name: 'Name',
							digits: 'Digits',
							symbol: 'Symbol',
						}).map(
							([ key, name ]) => (
								<React.Fragment key={key}>
									<dt>{name}</dt>
									<dd>{String(currency[key])}</dd>
								</React.Fragment>
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
				</Box.Body>
			</Box>
		);
	}
}

export default connect(
	state => ({
		currency: state.money.currencies.activeObject,
	})
)(CurrencyDetail);
