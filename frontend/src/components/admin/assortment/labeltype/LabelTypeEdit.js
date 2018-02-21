import React from 'react';
import { connect } from 'react-redux';
import { createLabelType, updateLabelType } from '../../../../state/assortment/label-types/actions.js';
import Form from '../../../forms/Form';
import StringField from '../../../forms/StringField';
import SelectField from '../../../forms/SelectField';
import { fetchLabelType, setLabelTypeField } from '../../../../state/assortment/label-types/actions';

class LabelTypeEdit extends React.Component {
	setName = ({ target: { value }}) => this.props.setLabelTypeField('name', value);
	setDescription = ({ target: { value }}) => this.props.setLabelTypeField('description', value);
	setUnitType = ({ target: { value }}) => this.props.setLabelTypeField('unit_type', Number(value));

	componentWillMount() {
		this.props.fetchLabelType(this.props.id);
	}

	reset = () => this.props.fetchLabelType(this.props.id);

	submit(evt) {
		evt.preventDefault();
		if (this.props.labelType.id === null) {
			this.props.createLabelType(this.props.labelType);
		} else {
			this.props.updateLabelType(this.props.labelType);
		}
	}

	componentWillReceiveProps(props) {
		if (props.id !== this.props.id) {
			this.props.fetchLabelType(this.props.id);
		}
	}

	render() {
		const { labelType, errorMsg, unitTypes } = this.props;

		return (
			<Form
				title={`${labelType.id === null ? 'Add' : 'Edit'} label type`}
				onSubmit={this.submit}
				onReset={this.reset}
				error={errorMsg}
				returnLink={labelType.id === null ? '/assortment/' : `/assortment/labeltype/${labelType.id}/`}
				closeLink="/assortment/">
				<StringField
					onChange={this.setName}
					value={labelType.name}
					name="Name" />
				<StringField
					onChange={this.setDescription}
					value={labelType.description}
					name="Description" />
				<SelectField
					disabled={!!labelType.id}
					onChange={this.setUnitType}
					value={labelType.unit_type}
					name="Unit type"
					options={unitTypes}
					nameField="type_long" />
			</Form>
		);
	}
}

export default connect(
	state => ({
		errorMsg: state.assortment.labelTypes.inputError,
		labelType: state.assortment.labelTypes.activeObject,
		unitTypes: state.assortment.unitTypes.unitTypes,
	}),
	{
		createLabelType,
		updateLabelType,
		fetchLabelType,
		setLabelTypeField,
	}
)(LabelTypeEdit);
