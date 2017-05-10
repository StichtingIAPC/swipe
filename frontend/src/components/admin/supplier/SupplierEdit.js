import React from "react";
import { connect } from "react-redux";
import { createSupplier, updateSupplier } from "../../actions/suppliers";
import Form from "../forms/Form";
import { StringField } from "../forms/fields";

class SupplierEdit extends React.Component {
	constructor(props) {
		super(props);
		this.state = this.getResetState();
	}

	componentWillMount() {
		this.reset(undefined, this.props);
	}

	getResetState(props = this.props) {
		if (props.supplier != null) return { ...props.supplier };
		return { id: null, name: '', notes: '', searchUrl: '' };
	}

	reset(evt, props) {
		if (evt) evt.preventDefault();
		this.setState(this.getResetState(props));
	}

	submit(evt) {
		evt.preventDefault();
		if (this.state.id == null) {
			this.props.addSupplier({ ...this.state, lastModified: new Date() });
		} else {
			this.props.editSupplier({ ...this.state, lastModified: new Date() });
		}
	}

	componentWillReceiveProps(props) {
		if (this.props.supplier != props.supplier) this.reset(undefined, props);
	}

	render() {
		const updateValue = key => evt => this.setState({ [key]: evt.target.value });

		return (
			<Form
				title={((typeof this.state.id === 'number') ? 'Edit' : 'Add') + " supplier"}
				onSubmit={this.submit.bind(this)}
				onReset={this.reset.bind(this)}
				error={this.props.errorMsg}
				returnLink={this.props.supplier ? `/supplier/${this.props.supplier.id}/` : '/supplier/'}
				closeLink="/supplier/">
				<StringField onChange={updateValue('name')} value={this.state.name} name="Name" />
				<StringField onChange={updateValue('notes')} value={this.state.notes} name="Notes" />
				<StringField onChange={updateValue('searchUrl')} value={this.state.searchUrl} name="Search Url" />
			</Form>
		)
	}
}

function mapStateToProps(state, ownProps) {
	return {	supplier: (state.suppliers.suppliers || []).filter(s => s.id === parseInt(ownProps.params.supplierID || '-1'))[0] };
}

export default connect(
	mapStateToProps,
	dispatch => ({
		addSupplier: supplier => dispatch(createSupplier(supplier)),
		editSupplier: supplier => dispatch(updateSupplier(supplier)),
	})
)(SupplierEdit);