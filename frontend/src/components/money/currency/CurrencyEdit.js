import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { createCurrency, updateCurrency, resetCurrency, fetchCurrency, setCurrencyField } from '../../../state/money/currencies/actions.js';
import Form from '../../forms/Form';
import { CharField, IntegerField, MoneyField, StringField } from '../../forms/fields';
import FontAwesome from '../../tools/icons/FontAwesome';

/**
 * Created by Matthias on 26/11/2016.
 */

class CurrencyEdit extends React.Component {
	reset = (currencyID = this.props.match.params.currencyID) => {
		const currencyId = typeof currencyID === 'object' ? this.props.match.params.currencyID : currencyID;

		if (typeof currencyId === 'undefined' || currencyId === null) {
			this.props.resetCurrency();
		} else {
			this.props.fetchCurrency(currencyId);
		}
	};

	componentWillMount() {
		this.reset();
	}

	componentWillReceiveProps({ match: { params: { currencyID }}}) {
		if (currencyID !== this.props.match.params.currencyID) {
			this.reset(currencyID);
		}
	}

	update = () => this.props.updateCurrency(this.props.currency);
	create = () => this.props.createCurrency(this.props.currency);

	setName = ({ target: { value }}) => this.props.setCurrencyField('name', value);
	setDigits = ({ target: { value }}) => this.props.setCurrencyField('digits', value);
	setSymbol = ({ target: { value }}) => this.props.setCurrencyField('symbol', value);
	setIso = ({ target: { value }}) => this.props.setCurrencyField('iso', value);

	addDenomination = () => this.props.setCurrencyField('denomination_set', this.props.currency.denomination_set.concat([{ amount: '' }]));

	render() {
		const { currency } = this.props;

		const updateDenom = index =>
			({ target: { value }}) => {
				this.props.setCurrencyField(
					'denomination_set',
					this.props.currency.denomination_set.map((el, i) => {
						if (i === index) {
							return {
								...el,
								amount: value,
							};
						}
						return el;
					})
				);
			};

		const removeDenom = index => () => this.props.setCurrencyField('denomination_set', this.props.currency.denomination_set.filter((_, i) => i !== index));

		return (
			<Form
				title={this.props.match.params.currencyID ? `Edit ${this.props.currency.name}` : 'Create new currency'}
				onReset={this.reset}
				onSubmit={this.props.match.params.currencyID ? this.update : this.create}
				error={this.props.errorMsg}
				returnLink={this.props.match.params.currencyID ? `/money/currency/${currency.iso}/` : '/money/'}
				closeLink="/money/">
				<CharField disabled={this.props.match.params.currencyID} onChange={this.setIso} name="ISO value" value={currency.iso} minLength={3} maxLength={3} />
				<StringField onChange={this.setName} name="Name" value={currency.name} />
				<IntegerField min={-23} max={5} onChange={this.setDigits} name="digits" value={currency.digits} />
				<CharField disabled={this.props.match.params.currencyID} onChange={this.setSymbol} name="Currency symbol" value={currency.symbol} minLength={1} maxLength={5} />
				<div className="form-group">
					<label className="col-sm-3 control-label">Denominations</label>
					<div className="col-sm-9">
						{currency.denomination_set.map((denomination, index) => (
							<div key={denomination.id || index} className="">
								<MoneyField
									currency={currency}
									value={denomination.amount}
									{...(
										denomination.id ?
											{ disabled: true } :
											{ onChange: updateDenom(index) })
									}>
									{denomination.id ? null : (
										<span className="input-group-btn">
											<a className="btn btn-danger" onClick={removeDenom(index)}>
												<FontAwesome icon="trash" />
											</a>
										</span>
									)}
								</MoneyField>
								<br />
							</div>
						))}
						<a className="btn btn-success" onClick={this.addDenomination}>Add denomination</a>
					</div>
				</div>
			</Form>
		);
	}
}

export default connect(
	state => ({
		errorMsg: state.money.currencies.error,
		currency: state.money.currencies.activeObject,
	}),
	{
		updateCurrency,
		createCurrency,
		fetchCurrency,
		resetCurrency,
		clearCurrencyField: resetCurrency,
		setCurrencyField,
	}
)(CurrencyEdit);
