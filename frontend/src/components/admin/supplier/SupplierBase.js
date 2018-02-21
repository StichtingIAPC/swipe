import React from 'react';
import { connect } from 'react-redux';
import { Switch, Route } from 'react-router-dom';
import { connectMixin, fetchStateRequirementsFor } from '../../../core/stateRequirements';
import { suppliers } from '../../../state/suppliers/actions.js';
import SupplierList from './SupplierList';
import SupplierEdit from './SupplierEdit';
import SupplierDetail from './SupplierDetail';

class SupplierBase extends React.Component {
	componentWillMount() {
		fetchStateRequirementsFor(this);
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
	connectMixin({ suppliers })
)(SupplierBase);
