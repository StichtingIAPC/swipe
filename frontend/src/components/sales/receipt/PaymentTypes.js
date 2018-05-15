import React from 'react';
import PropTypes from 'prop-types';

export default class PaymentTypes extends React.Component {
	render() {
		return <div style={{ border: '1px solid black' }}>
			Payment type selector
		</div>;
	}
}

PaymentTypes.propTypes = {
	onPaymentTypesChanged: PropTypes.func.isRequired,
	paymentTypes: PropTypes.array.isRequired,
};
