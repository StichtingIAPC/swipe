import React from "react";
import {connect} from "react-redux";
import {Link, browserHistory} from "react-router";
import {updateCurrency} from "../../../actions/money/currencies";
import Form from "../../forms/Form";
import {StringField, IntegerField, CharField, MoneyInput} from "../../forms/fields";
import FontAwesome from "../../tools/icons/FontAwesome";

/**
 * Created by Matthias on 26/11/2016.
 */

class CurrencyEdit extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			currency: this.props.currency,
			workingCopy: {
				iso: 'invalid iso',
				name: 'PLACEHOLDER',
				digits: -1,
				symbol: '#####',
				...this.props.currency,
			},
		}
	}

	reset(evt) {
		this.setState({
			workingCopy: {...this.state.currency},
		})
	}

	update(evt) {
		evt.preventDefault();
		const obj = {...this.state.workingCopy};
		obj.lastModified = new Date();
		this.props.updateCurrency(obj);
		browserHistory.push(`/money/currency/${obj.iso}/`);
	}

	componentWillReceiveProps(nextProps) {
		if (this.state.currency != nextProps.currency) {
			this.setState({
				currency: nextProps.currency,
				workingCopy: {
					iso: 'invalid iso',
					name: 'PLACEHOLDER',
					digits: -1,
					symbol: '#####',
					...nextProps.currency,
				},
			});
		}
	}

	render() {
		const currency = this.state.workingCopy;
		const updateValue = (key) =>
			(evt) => this.setState({
				workingCopy: {
					...this.state.workingCopy,
					[key]: evt.target.value,
				},
			});

		const addDenomination = () => this.setState({
			workingCopy: {
				...this.state.workingCopy,
				denomination_set: [...this.state.workingCopy.denomination_set, {amount: ''}],
			},
		});

		const updateDenom = (index) => (
			(evt) => {
				const newDenoms = [...this.state.workingCopy.denomination_set];
				newDenoms[index].amount = evt.target.value;
				this.setState({
					workingCopy: {
						...this.state.workingCopy,
						denomination_set: newDenoms,
					},
				})
			}
		);

		const removeDenom = (index) => (
			(evt) => {
				const newDenoms = [...this.state.workingCopy.denomination_set];
				newDenoms.splice(index, 1);
				this.setState({
					workingCopy: {
						...this.state.workingCopy,
						denomination_set: [...newDenoms],
					},
				})
			}
		);

		return (
			<Form
				title={`Edit ${this.state.currency.name}`}
				onReset={this.reset.bind(this)}
				onSubmit={this.update.bind(this)}
				returnLink={`/money/currency/${currency.iso}/`}>
				<CharField disabled={true} onChange={updateValue('iso')} name="ISO value" value={currency.iso} minLength={3} maxLength={3} />
				<StringField onChange={updateValue('name')} name="Name" value={currency.name} />
				<IntegerField onChange={updateValue('digits')} name="digits" value={currency.digits} />
				<CharField disabled={true} onChange={updateValue('symbol')} name="Currency symbol" value={currency.symbol} minLength={1} maxLength={5} />
				<div className="form-group">
					<label className="col-sm-3 control-label">Denominations</label>
					<div className="col-sm-9">
						{currency.denomination_set.map((denomination, index) => (
							<div key={denomination.id} className="">
								<MoneyInput
									currency={currency}
									value={denomination.amount}
									{...(
										denomination.id ?
											{disabled: true} :
											{onChange: updateDenom(index)})
									}>
									{denomination.id ? null : (
										<span className="input-group-btn">
											<Link className="btn btn-danger" onClick={removeDenom(index)}>
												<FontAwesome icon="trash" />
											</Link>
										</span>
									)}
								</MoneyInput>
								<br />
							</div>
						))}
						<Link className="btn btn-success" onClick={addDenomination}>Add denomination</Link>
					</div>
				</div>
			</Form>
		)
	}
}

export default connect(
	(state, ownProps) => ({
		...ownProps,
		currency: Object.values(state.currencies.objects).find((obj) => obj.iso == ownProps.params.currencyID),
	}),
	(dispatch) => ({
		updateCurrency: (currency) => dispatch(updateCurrency(currency)),
	})
)(CurrencyEdit);
