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
		this.reset(null);
	}

	getResetState() {
		if (this.props.supplier != null) return { ...this.props.supplier };
		return { id: null, name: '', notes: '', searchUrl: '' };
	}

	reset(evt) {
		if (evt) evt.preventDefault();
		this.setState(this.getResetState());
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
		if (this.state.id === null && props.supplier != null && props.supplier.id != null) this.reset();
	}

	render() {
		const updateValue = key => evt => this.setState({ [key]: evt.target.value });

		return (
			<Form
				title={((typeof this.state.id === 'number') ? 'Edit' : 'Add') + " supplier"}
				onSubmit={this.submit.bind(this)}
				onReset={this.reset.bind(this)}
				returnLink={`/supplier/`}>
				<StringField onChange={updateValue('name')} value={this.state.name} name="Name" />
				<StringField onChange={updateValue('notes')} value={this.state.notes} name="Notes" />
				<StringField onChange={updateValue('searchUrl')} value={this.state.searchUrl} name="Search Url" />
			</Form>
		)
	}
};

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
