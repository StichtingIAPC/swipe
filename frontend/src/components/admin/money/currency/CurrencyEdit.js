import React from "react";
import { connect } from "react-redux";
import { Link } from "react-router";
import { createCurrency, updateCurrency } from "../../../actions/money/currencies";
import Form from "../../forms/Form";
import { CharField, IntegerField, MoneyField, StringField } from "../../forms/fields";
import FontAwesome from "../../tools/icons/FontAwesome";

/**
 * Created by Matthias on 26/11/2016.
 */

const defaultCurrency = {
	iso: '',
	name: '',
	digits: 2,
	symbol: '',
	denomination_set: [],
};

class CurrencyEdit extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			workingCopy: {
				...defaultCurrency,
				...this.props.currency,
			},
		};
	}

	reset(evt, props = this.props) {
		if (evt)
			evt.preventDefault();
		this.setState({
			workingCopy: {
				...defaultCurrency,
				...props.currency,
			},
		});
	}

	update(evt) {
		if (evt)
			evt.preventDefault();
		const obj = { ...this.state.workingCopy };

		obj.lastModified = new Date();
		this.props.updateCurrency(obj);
	}

	create(evt) {
		if (evt)
			evt.preventDefault();
		const obj = { ...this.state.workingCopy };

		obj.lastModified = new Date();
		this.props.createCurrency(obj);
	}

	componentWillReceiveProps(props) {
		if (this.props.currency !== props.currency)
			this.reset(null, props);
	}

	render() {
		const currency = this.state.workingCopy;

		const updateValue = key =>
			evt => this.setState({
				workingCopy: {
					...this.state.workingCopy,
					[key]: evt.target.value,
				},
			});

		const addDenomination = () => this.setState({
			workingCopy: {
				...this.state.workingCopy,
				denomination_set: [ ...this.state.workingCopy.denomination_set, { amount: '' }],
			},
		});

		const updateDenom = index =>
			evt => {
				const newDenoms = [ ...this.state.workingCopy.denomination_set ];

				newDenoms[index].amount = evt.target.value;
				this.setState({
					workingCopy: {
						...this.state.workingCopy,
						denomination_set: newDenoms,
					},
				});
			}

		;

		const removeDenom = index =>
			() => {
				const newDenoms = [ ...this.state.workingCopy.denomination_set ];

				newDenoms.splice(index, 1);
				this.setState({
					workingCopy: {
						...this.state.workingCopy,
						denomination_set: [ ...newDenoms ],
					},
				});
			};

		return (
			<Form
				title={this.props.currency ? `Edit ${this.props.currency.name}` : 'Create new currency'}
				onReset={::this.reset}
				onSubmit={this.props.currency ? ::this.update : ::this.create}
				error={this.props.errorMsg}
				returnLink={this.props.currency ? `/money/currency/${currency.iso}/` : '/money/'}
				closeLink="/money/">
				<CharField disabled={!!this.props.currency} onChange={updateValue('iso')} name="ISO value" value={currency.iso} minLength={3} maxLength={3} />
				<StringField onChange={updateValue('name')} name="Name" value={currency.name} />
				<IntegerField min={-23} max={5} onChange={updateValue('digits')} name="digits" value={currency.digits} />
				<CharField disabled={!!this.props.currency} onChange={updateValue('symbol')} name="Currency symbol" value={currency.symbol} minLength={1} maxLength={5} />
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
											<Link className="btn btn-danger" onClick={removeDenom(index)}>
												<FontAwesome icon="trash" />
											</Link>
										</span>
									)}
								</MoneyField>
								<br />
							</div>
						))}
						<Link className="btn btn-success" onClick={addDenomination}>Add denomination</Link>
					</div>
				</div>
			</Form>
		);
	}
}

export default connect(
	(state, ownProps) => ({
		...ownProps,
		errorMsg: state.currencies.inputError,
		currency: (state.currencies.currencies || []).find(obj => obj.iso === ownProps.params.currencyID) || null,
	}),
	dispatch => ({
		updateCurrency: currency => dispatch(updateCurrency(currency)),
		createCurrency: currency => dispatch(createCurrency(currency)),
	})
)(CurrencyEdit);
