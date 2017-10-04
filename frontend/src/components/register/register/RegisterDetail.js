import React from "react";
import PropTypes from "prop-types";
import { Link } from "react-router";
import { connect } from "react-redux";
import FontAwesome from "../../tools/icons/FontAwesome";

class RegisterDetail extends React.Component {
	trash(evt) {
		evt.preventDefault();
	}

	render() {
		const { register } = this.props;

		if (!register)
			return null;

		return (
			<div className="box">
				<div className="box-header with-border">
					<h3 className="box-title">Register: {register.name}</h3>
					<div className="box-tools">
						<div className="input-group">
							<div className="btn-group">
								<Link to="/register/" className="btn btn-default btn-sm" title="Close"><FontAwesome icon="close" /></Link>
								<Link to={`/register/register/${register.id}/edit/`} className="btn btn-default btn-sm" title="Edit"><FontAwesome icon="edit" /></Link>
								<Link onClick={::this.trash} className="btn btn-danger btn-sm" title="Delete"><FontAwesome icon="trash" /></Link>
							</div>
						</div>
					</div>
				</div>
				<div className="box-body">
					<dl className="dl-horizontal">
						{[ 'name', 'is_cash_register', 'is_active', 'currency' ].map(
							key => (
								<div key={key}>
									<dt>{key}</dt>
									<dd>{String(register[key])}</dd>
								</div>
							)
						)}
						<div>
							<dt>Payment type</dt>
							<dd>{this.props.paymentType.name}</dd>
						</div>
					</dl>
				</div>
			</div>
		);
	}
}

RegisterDetail.propTypes = { params: PropTypes.shape({ registerID: PropTypes.string.isRequired }).isRequired };

export default connect(
	(state, ownProps) => {
		// TODO: use fetch method
		const register = state.register.registers.registers.filter(s => +s.id === +ownProps.params.registerID)[0];

		return {
			register,
			paymentType: state.register.paymentTypes.paymentTypes.find(s => +s.id === register.payment_type),
		};
	}
)(RegisterDetail);
