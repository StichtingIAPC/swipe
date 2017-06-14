import React from "react";
import { connect } from "react-redux";
import { connectMixin, fetchStateRequirementsFor } from "../../../core/stateRequirements";
import { suppliers } from "../../../actions/suppliers";
import SupplierList from "./SupplierList";

class SupplierBase extends React.Component {
	componentWillMount() {
		fetchStateRequirementsFor(this);
	}

	render() {
		return (
			<div className="row">
				<div className="col-xs-4 col-md-4">
					<SupplierList supplierID={this.props.params.supplierID || ''} />
				</div>
				<div className="col-xs-8 col-md-8">
					{this.props.requirementsLoaded ? this.props.children : null}
				</div>
			</div>
		);
	}
}

export default connect(
	connectMixin({ suppliers })
)(SupplierBase);
