import React from "react";
import {connect} from "react-redux";
import {browserHistory} from "react-router";
import {createCurrency} from "../../../actions/money/currencies";
import Form from "../../forms/Form";
import {StringField, IntegerField, CharField} from "../../forms/fields";

/**
 * Created by Matthias on 26/11/2016.
 */

class CurrencyCreate extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			workingCopy: {
				iso: '',
				name: '',
				digits: 0,
				symbol: '',
			},
		}
	}

	reset(evt) {
		this.setState({
			workingCopy: {
				iso: '',
				name: '',
				digits: 0,
				symbol: '',
			},
		})
	}

	create(evt) {
		evt.preventDefault();
		const obj = {...this.state.workingCopy};
		obj.lastModified = new Date();
		this.props.create(obj);
		browserHistory.push('/money/');
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
		return (
			<Form
				title="Create new currency"
				onReset={this.reset.bind(this)}
				onSubmit={this.create.bind(this)}
				returnLink="/money/">
				<CharField onChange={updateValue('iso')} name="ISO value" value={currency.iso} minLength={3} maxLength={3} />
				<StringField onChange={updateValue('name')} name="Name" value={currency.name} />
				<IntegerField onChange={updateValue('digits')} name="digits" value={currency.digits} />
				<CharField onChange={updateValue('symbol')} name="Currency symbol" value={currency.symbol} />
			</Form>
		)
	}
}

export default connect(
	(state, ownProps) => ({
		...ownProps,
	}),
	(dispatch, ownProps) => ({
		...ownProps,
		create: (currency) => dispatch(createCurrency(currency)),
	})
)(CurrencyCreate);
