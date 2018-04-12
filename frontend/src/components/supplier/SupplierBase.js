import React from 'react';
import { connect } from 'react-redux';
import { Route, Switch } from 'react-router-dom';
import SupplierList from './SupplierList';
import SupplierEdit from './SupplierEdit';
import SupplierDetail from './SupplierDetail';
import { fetchAllSuppliers } from '../../state/suppliers/actions';
import { getSupplierData, getSupplierLoading, getSupplierPopulated } from '../../state/suppliers/selectors';

class SupplierBase extends React.Component {
	static getDerivedStateFromProps(nextProps) {
		if (!nextProps.isPopulated && !nextProps.isLoading) {
			nextProps.fetchExternalisations();
		}
	}

	render() {
		const { match } = this.props;

		return (
			<div className="row">
				<div className="col-xs-4 col-md-4">
					<SupplierList supplierID={match.params.supplierID || ''} />
				</div>
				<div className="col-xs-8 col-md-8">
					{
						this.props.requirementsLoaded ? (
							<Switch>
								<Route key="new" path={`${match.path}/create`} component={SupplierEdit} />
								<Route key="old" path={`${match.path}/:supplierID/edit`} component={SupplierEdit} />
								<Route key="old" path={`${match.path}/:supplierID`} component={SupplierDetail} />
							</Switch>
						) : null
					}
				</div>
			</div>
		);
	}
}

export default connect(
	state => ({
		suppliers: getSupplierData(state),
		isLoading: getSupplierLoading(state),
		isPopulated: getSupplierPopulated(state),
	}),
	{ fetchSuppliers: fetchAllSuppliers },
)(SupplierBase);

