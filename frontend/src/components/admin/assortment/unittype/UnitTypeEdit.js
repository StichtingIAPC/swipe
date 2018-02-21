import React from 'react';
import { connect } from 'react-redux';
import { createUnitType, updateUnitType } from '../../../../state/assortment/unit-types/actions.js';
import Form from '../../../forms/Form';
import StringField from '../../../forms/StringField';
import SelectField from '../../../forms/SelectField';
import { incrementalTypes, valueTypes } from '../../../../state/assortment/constants';
import { fetchUnitType, setUnitTypeField } from '../../../../state/assortment/unit-types/actions';

class UnitTypeEdit extends React.Component {
	componentWillMount() {
		this.reset(null);
	}

	setTypeLong = ({ target: { value }}) => this.props.setUnitTypeField('type_long', value);
	setTypeShort = ({ target: { value }}) => this.props.setUnitTypeField('type_short', value);
	setValueType = ({ target: { value }}) => this.props.setUnitTypeField('value_type', value);
	setIncrementalType = ({ target: { value }}) => this.props.setUnitTypeField('incremental_type', value);

	reset = evt => {
		if (evt) {
			evt.preventDefault();
		}
		this.props.fetchUnitType(this.props.id);
	};

	submit = evt => {
		evt.preventDefault();
		if (this.props.id === 'new') {
			this.props.createUnitType(this.props.unitType);
		} else {
			this.props.updateUnitType(this.props.unitType);
		}
	};

	componentWillReceiveProps(props) {
		if (props.id !== this.props.id) {
			this.props.fetchUnitType(props.id);
		}
	}

	render() {
		const { unitType, errorMsg, id } = this.props;

		return (
			<Form
				title={`${typeof unitType.id === 'number' ? 'Edit' : 'Add'} unit type`}
				onSubmit={this.submit}
				onReset={this.reset}
				error={errorMsg}
				returnLink={id === 'new' ? '/assortment/' : `/assortment/unittype/${unitType.id}/`}
				closeLink="/assortment/">
				<StringField
					onChange={this.setTypeLong}
					value={unitType.type_long}
					name="Long type name (eg. meter)" />
				<StringField
					onChange={this.setTypeShort}
					value={unitType.type_short}
					name="Short type name (eg. m)" />
				<SelectField
					disabled={!!unitType.id}
					onChange={this.setValueType}
					value={unitType.value_type || ' '}
					name="Value type"
					options={valueTypes} />
				<SelectField
					onChange={this.setIncrementalType}
					value={unitType.incremental_type || ' '}
					name="Incrementing using"
					options={incrementalTypes} />
			</Form>
		);
	}
}

export default connect(
	state => ({
		errorMsg: state.assortment.unitTypes.inputError,
		unitType: state.assortment.unitTypes.activeObject,
	}),
	{
		fetchUnitType,
		createUnitType,
		updateUnitType,
		setUnitTypeField,
	},
)(UnitTypeEdit);
