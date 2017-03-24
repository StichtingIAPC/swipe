import React from "react";
import { connect } from "react-redux";
import { Link } from "react-router";
import { createUnitType, updateUnitType } from "../../../actions/assortment/unitTypes";
import Form from "../../forms/Form";
import StringField from "../../forms/StringField";
import SelectField from "../../forms/SelectField";
import { valueTypes, incrementalTypes } from "../../../constants/assortment";

class UnitTypeEdit extends React.Component {
	constructor(props) {
		super(props);
		this.state = this.getResetState();
	}

	componentWillMount() {
		this.reset(undefined, this.props);
	}

	getResetState(props = this.props) {
		if (props.unitType != null) return {...props.unitType};
		return {id: null, type_long: '', type_short: '', value_type: null, incremental_type: null};
	}

	reset(evt, props) {
		if (evt) evt.preventDefault();
		this.setState(this.getResetState(props));
	}

	submit(evt) {
		evt.preventDefault();
		if (this.state.id === null) {
			this.props.addUnitType({...this.state});
		} else {
			this.props.editUnitType({...this.state});
		}
	}

	componentWillReceiveProps(props){
		this.reset(undefined, props);
	}

	render() {
		return (
			<Form
				title={((typeof this.state.id === 'number') ? 'Edit' : 'Add') + " unit type"}
				onSubmit={this.submit.bind(this)}
				onReset={this.reset.bind(this)}
				error={this.props.errorMsg}
				returnLink={this.props.supplier ? `/assortment/labeltype/${this.props.labelType.id}/` : '/assortment/'}
				closeLink="/assortment/">
				<StringField onChange={(evt) => this.setState({type_long: evt.target.value})} value={this.state.type_long} name="Long type name (eg. meter)" />
				<StringField onChange={(evt) => this.setState({type_short: evt.target.value})} value={this.state.type_short} name="Short type name (eg. m)" />
				<SelectField disabled={!!this.state.id} onChange={(evt) => this.setState({value_type: evt.target.value})} value={this.state.value_type || ' '} name="Value type" options={valueTypes} />
				<SelectField onChange={(evt) => this.setState({incremental_type: evt.target.value})} value={this.state.incremental_type || ' '} name="Incrementing using" options={incrementalTypes} />
			</Form>
		);
	}
}

export default connect(
	(state, props) => ({
		errorMsg: state.unitTypes.inputError,
		unitType: (state.unitTypes.unitTypes || []).find(el => el.id === Number(props.params.unitTypeID)),
	}),
	dispatch => ({
		addUnitType: (arg) => dispatch(createUnitType(arg)),
		editUnitType: (arg) => dispatch(updateUnitType(arg)),
	}),
)(UnitTypeEdit);
