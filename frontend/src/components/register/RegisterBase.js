import React from 'react';
import { connect } from 'react-redux';
import { Switch, Route } from 'react-router-dom';
import { connectMixin, fetchStateRequirementsFor } from '../../core/stateRequirements';
import { registers } from '../../state/register/registers/actions.js';
import RegisterList from './register/RegisterList';
import PaymentTypeList from './paymentType/PaymentTypeList';
import { currencies } from '../../state/money/currencies/actions.js';
import { paymentTypes } from '../../state/register/payment-types/actions.js';
import RegisterEdit from './register/RegisterEdit';
import RegisterDetail from './register/RegisterDetail';
import PaymentTypeEdit from './paymentType/PaymentTypeEdit';
import PaymentTypeDetail from './paymentType/PaymentTypeDetail';

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
					{
						this.props.requirementsLoaded ? (
							<Switch>
								<Route path="register/create/" component={RegisterEdit} />
								<Route path="register/:registerID/edit/" component={RegisterEdit} />
								<Route path="register/:registerID/" component={RegisterDetail} />
								<Route path="paymenttype/create/" component={PaymentTypeEdit} />
								<Route path="paymenttype/:paymentTypeID/edit/" component={PaymentTypeEdit} />
								<Route path="paymenttype/:paymentTypeID/" component={PaymentTypeDetail} />
							</Switch>
						) : null
					}
				</div>
			</div>
		);
	}
}

export default connect(
	connectMixin({
		register: {
			registers,
			paymentTypes,
		},
		money: {
			currencies,
		},
	})
)(RegisterBase);
