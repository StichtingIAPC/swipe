import React from "react";
import { connect } from "react-redux";
import { connectMixin, fetchStateRequirementsFor } from "../../core/stateRequirements";
import { registers } from "../../actions/register/registers";
import RegisterList from "./register/RegisterList";
import PaymentTypeList from "./paymentType/PaymentTypeList";
import { currencies } from "../../actions/money/currencies";
import { paymentTypes } from "../../actions/register/paymentTypes";

class RegisterBase extends React.Component {
	componentWillMount() {
		fetchStateRequirementsFor(this);
	}

	render() {
		return (
			<div className="row">
				<div className="col-xs-4 col-md-4">
					<RegisterList supplierID={this.props.params.registerID || ''} />
					<PaymentTypeList paymentTypeID={this.props.params.paymentTypeID || ''} />
				</div>
				<div className="col-xs-8 col-md-8">
					{this.props.requirementsLoaded ? this.props.children : null}
				</div>
			</div>
		)
	}
}

export default connect(
	connectMixin({
		registers,
		paymentTypes,
		currencies,
	})
)(RegisterBase)
