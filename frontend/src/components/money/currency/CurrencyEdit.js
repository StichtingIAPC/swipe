import React from 'react';
import { connect } from 'react-redux';
import {
	createCurrency,
	updateCurrency,
	resetCurrency,
	fetchCurrency,
	setCurrencyField
} from '../../../state/money/currencies/actions.js';
import Card from '../../base/Card';
import { CharField, IntegerField, MoneyField, StringField } from '../../forms/fields';
import { hasError } from '../../../tools/validations/validators';
import { Button, ButtonToolbar, ControlLabel, FormControl, FormGroup, HelpBlock } from 'react-bootstrap';
import { getCurrencyValidations } from '../../../state/money/currencies/selectors';

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

	submit = evt => {
		evt.preventDefault();

		if (!this.props.match.params.currencyID) {
			this.props.createCurrency(this.props.currency);
		} else {
			this.props.updateCurrency(this.props.currency);
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

	addDenomination = () => this.props.setCurrencyField(
		'denomination_set',
		this.props.currency.denomination_set.concat([{
			amount: '',
			currency: this.props.match.params.currencyID ? this.props.currency.iso : null,
		}]));

	render() {
		const { currency } = this.props;

		const updateDenom = index =>
			value => {
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
		const iso_name = this.props.validations ? this.props.validations['iso'] : {};
		const isoValidation = iso_name ? iso_name.text : '';
		const isoErrorType = iso_name ? iso_name.type : 'success';

		const nameName = this.props.validations ? this.props.validations['name'] : {};
		const nameValidation = nameName ? nameName.text : '';
		const nameErrorType = nameName ? nameName.type : 'success';

		const digitError = this.props.validations ? this.props.validations['digits'] : {};
		const digitValidation = digitError ? digitError.text : '';
		const digitErrorType = digitError ? digitError.type : 'success';

		const removeDenom = index => () => this.props.setCurrencyField('denomination_set', this.props.currency.denomination_set.filter((_, i) => i !== index));

		return (
			<Card
				title={this.props.match.params.currencyID ? `Edit ${this.props.currency.name}` : 'Create new currency'}
				onReset={this.reset}
				error={this.props.errorMsg}
				returnLink={this.props.match.params.currencyID ? `/money/currency/${currency.iso}/` : '/money/'}
				closeLink="/money/">
				<form>
					<FormGroup
						controlId="formBasicText"
						validationState={isoErrorType}>
						<ControlLabel>ISO</ControlLabel>
						<FormControl
							disabled={this.props.match.params.currencyID}
							type="text"
							value={currency.iso}
							placeholder="ISO value"
							onChange={this.setIso} />
						<FormControl.Feedback />
						<HelpBlock>{isoValidation}</HelpBlock>
					</FormGroup>
					<FormGroup
						controlId="formBasicText"
						validationState={nameErrorType}>
						<ControlLabel>Name</ControlLabel>
						<FormControl
							type="text"
							value={currency.name}
							placeholder="Name"
							name="name"
							onChange={this.setName} />
						<FormControl.Feedback />
						<HelpBlock>{nameValidation}</HelpBlock>
					</FormGroup>

					<FormGroup
						controlId="formBasicText"
						validationState={digitErrorType}>
						<ControlLabel>Digits</ControlLabel>
						<FormControl
							type="number"
							value={currency.digits}
							placeholder="2"
							name="Digits"
							onChange={this.setDigits} />
						<FormControl.Feedback />
						<HelpBlock>{digitValidation}</HelpBlock>
					</FormGroup>
					<CharField
						disabled={this.props.match.params.currencyID} onChange={this.setSymbol}
						name="Currency symbol" value={currency.symbol} minLength={1} maxLength={5} />
					<div className="form-group">
						<label className="col-sm-3 control-label">Denominations</label>
						<div className="col-sm-9">
							{currency.denomination_set.map((denomination, index) => (
								<div key={denomination.id || index} className="">
									<MoneyField
										currency={currency.iso}
										value={denomination.amount}
										{...(
											denomination.id ?
												{ disabled: true } :
												{ onChange: updateDenom(index) })
										} />
									<br />
								</div>
							))}
							<a className="btn btn-success" onClick={this.addDenomination}>Add denomination</a>
						</div>
					</div>
					<ButtonToolbar>
						<Button
							bsStyle="success"
							onClick={this.submit}
							disabled={hasError(this.props.validations)}>Save</Button>
					</ButtonToolbar>
				</form>
			</Card>
		);
	}
}

export default connect(
	state => ({
		errorMsg: state.money.currencies.error,
		currency: state.money.currencies.activeObject,
		validations: getCurrencyValidations(state),
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
