import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router';
import { connect } from 'react-redux';
import FontAwesome from '../../tools/icons/FontAwesome';

class PaymentTypeDetail extends React.Component {
	static propTypes = {
		params: PropTypes.shape({
			paymentTypeID: PropTypes.string.isRequired,
		}).isRequired,
	};

	trash(evt) {
		evt.preventDefault();
	}

	render() {
		const { paymentType } = this.props;

		if (!paymentType)
			return null;

		return (
			<div className="box">
				<div className="box-header with-border">
					<h3 className="box-title">Payment type: {paymentType.name}</h3>
					<div className="box-tools">
						<div className="input-group">
							<div className="btn-group">
								<Link to="/register/" className="btn btn-default btn-sm" title="Close"><FontAwesome icon="close" /></Link>
								<Link to={`/register/paymenttype/${paymentType.id}/edit/`} className="btn btn-default btn-sm" title="Edit"><FontAwesome icon="edit" /></Link>
								<Link onClick={::this.trash} className="btn btn-danger btn-sm" title="Delete"><FontAwesome icon="trash" /></Link>
							</div>
						</div>
					</div>
				</div>
				<div className="box-body">
					<dl className="dl-horizontal">
						{[ 'name', 'is_invoicing' ].map(
							key => (
								<div key={key}>
									<dt>{key}</dt>
									<dd>{String(paymentType[key])}</dd>
								</div>
							)
						)}
					</dl>
				</div>
			</div>
		);
	}
}

export default connect(
	(state, ownProps) => ({
		...ownProps,
		paymentType: state.paymentTypes.paymentTypes.filter(s => +s.id === parseInt(ownProps.params.paymentTypeID || '-1', 10))[0],
	})
)(PaymentTypeDetail);
