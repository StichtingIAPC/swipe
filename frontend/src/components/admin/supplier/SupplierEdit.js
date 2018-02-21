import React from 'react';
import { connect } from 'react-redux';
import { createSupplier, updateSupplier } from '../../../state/suppliers/actions.js';
import Form from '../../forms/Form';
import { StringField } from '../../forms/fields';
import { fetchSupplier, newSupplier, setSupplierField } from '../../../state/suppliers/actions';

class SupplierEdit extends React.Component {
	componentWillMount() {
		if (this.props.match.params.supplierID) {
			this.props.fetchSupplier(this.props.match.params.supplierID);
		} else {
			this.props.newSupplier();
		}
	}

	componentWillReceiveProps({ match }) {
		if (this.props.match.params.supplierID !== match.params.supplierID) {
			if (Number.isNaN(+match.params.supplierID)) {
				this.props.newSupplier();
			} else {
				this.props.fetchSupplier(match.params.supplierID);
			}
		}
	}

	submit = (evt) => {
		evt.preventDefault();
		if (this.props.supplier.id === null) {
			this.props.createSupplier(this.props.supplier);
		} else {
			this.props.updateSupplier(this.props.supplier);
		}
	};

	reset = () => {
		if (this.props.supplier.id === null) {
			this.props.newSupplier();
		} else {
			this.props.fetchSupplier(this.props.supplier.id);
		}
	};

	setName = ({ target: { value }}) => this.props.setSupplierField('name', value);
	setNotes = ({ target: { value }}) => this.props.setSupplierField('notes', value);
	setSearch_url = ({ target: { value }}) => this.props.setSupplierField('search_url', value);

	render() {
		const { supplier } = this.props;
		const NEW = supplier.id === null;

		return (
			<Form
				title={`${NEW ? 'Add' : 'Edit'} supplier`}
				onSubmit={this.submit}
				onReset={this.reset}
				error={this.props.errorMsg}
				returnLink={NEW ? '/supplier/' : `/supplier/${supplier.id}`}
				closeLink="/supplier/">
				<StringField onChange={this.setName} value={supplier.name} name="Name" />
				<StringField onChange={this.setNotes} value={supplier.notes} name="Notes" />
				<StringField onChange={this.setSearch_url} value={supplier.search_url} name="Search Url" />
			</Form>
		);
	}
}

const mapStateToProps = state => ({
	supplier: state.suppliers.activeObject,
});

export default connect(
	mapStateToProps,
	{
		fetchSupplier,
		newSupplier,
		createSupplier,
		updateSupplier,
		setSupplierField,
	}
)(SupplierEdit);
