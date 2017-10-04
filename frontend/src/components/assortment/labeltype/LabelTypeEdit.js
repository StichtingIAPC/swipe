import React from 'react';
import { connect } from 'react-redux';
import { createLabelType, updateLabelType } from '../../../state/assortment/label-types/actions.js';
import Form from '../../forms/Form';
import StringField from '../../forms/StringField';
import SelectField from '../../forms/SelectField';

class LabelTypeEdit extends React.Component {
	constructor(props) {
		super(props);
		this.state = this.getResetState();
	}

	componentWillMount() {
		this.reset(null, this.props);
	}

	getResetState(props = this.props) {
		if (props.labelType !== null)
			return { ...props.labelType };
		return {
			id: null,
			name: '',
			description: '',
			unit_type: null,
			labels: [],
		};
	}

	reset(evt, props) {
		if (evt)
			evt.preventDefault();
		this.setState(this.getResetState(props));
	}

	submit(evt) {
		evt.preventDefault();
		if (this.state.id === null)
			this.props.addLabelType({ ...this.state });
		 else
			this.props.editLabelType({ ...this.state });
	}

	componentWillReceiveProps(props) {
		this.reset(null, props);
	}

	render() {
		return (
			<Form
				title={`${typeof this.state.id === 'number' ? 'Edit' : 'Add'} label type`}
				onSubmit={::this.submit}
				onReset={::this.reset}
				error={this.props.errorMsg}
				returnLink={this.props.supplier ? `/assortment/labeltype/${this.props.labelType.id}/` : '/assortment/'}
				closeLink="/assortment/">
				<StringField
					onChange={evt => this.setState({ name: evt.target.value })}
					value={this.state.name}
					name="Name" />
				<StringField
					onChange={evt => this.setState({ description: evt.target.value })}
					value={this.state.description}
					name="Description" />
				<SelectField
					disabled={!!this.state.id}
					onChange={evt => this.setState({ unit_type: Number(evt.target.value) })}
					value={this.state.unit_type || 1}
					name="Unit type"
					options={this.props.unitTypes}
					nameField="type_long" />
			</Form>
		);
	}
}

export default connect(
	(state, props) => ({
		errorMsg: state.assortment.labelTypes.inputError,
		// TODO: Replace find with object fetch
		labelType: state.assortment.labelTypes.labelTypes.find(el => el.id === +props.params.labelTypeID),
		unitTypes: state.assortment.unitTypes.unitTypes,
	}),
	{
		addLabelType: createLabelType,
		editLabelType: updateLabelType,
	}
)(LabelTypeEdit);
