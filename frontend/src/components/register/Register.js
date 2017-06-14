import React from 'react';
import { connect } from 'react-redux';
import Step from './Step.js';
import ClientSelection from './ClientSelection.js';
import { setClientType } from '../../actions/register.js';

export default connect(
	state => ({
		step: state.register.step,
		cart: state.register.cart,
		client: state.register.client,
	}),
	dispatch => ({
		updateClientType: type => dispatch(setClientType(type)),
	})
)(class Register extends React.Component {

	render() {
		const { step, cart } = this.props;
		return <div className="row">
			<div className="col-xs-6 col-md-6">

			</div>
			<div className="col-xs-6 col-md-6 register">
				<Step name="Client" active={step == 'client'}>
					<ClientSelection
						type={this.props.client.type}
						updateType={this.props.updateClientType} />
				</Step>
				<Step name="Cart" active={step == 'cart'}>
					<span>hoi</span>
				</Step>
				<Step name="Coin" active={step == 'coin'}>
					<span>hoi</span>
				</Step>
				<Step name="Care" active={step == 'care'}>
					<span>hoi</span>
				</Step>
			</div>
		</div>;
	}

});
