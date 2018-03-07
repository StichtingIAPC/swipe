import React from 'react';

export default class PaymentButton extends React.Component {

	render() {
		return (
			<div>
				<button onClick={this.transaction} className="btn btn-default">Pay</button>
			</div>
		);
	}

	transaction() {

	}



}