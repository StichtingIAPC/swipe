import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Link } from 'react-router';
import FontAwesome from '../../tools/icons/FontAwesome';

class VATDetail extends React.Component {
	static propTypes = {
		vat: PropTypes.shape({
			id: PropTypes.number.isRequired,
			name: PropTypes.string.isRequired,
			active: PropTypes.bool.isRequired,
			vatperiod_set: PropTypes.arrayOf(PropTypes.number).isRequired,
		}),
	};

	trash() {
		return null;
	}

	render() {
		const vat = this.props.VAT;

		if (!vat)
			return null;

		return (
			<div className="box">
				<div className="box-header with-border">
					<h3 className="box-title">VAT: {vat.name}</h3>
					<div className="box-tools">
						<div className="input-group">
							<div className="btn-group">
								<Link to={`/money/vat/${vat.id}/edit/`} className="btn btn-default btn-sm" title="Edit"><FontAwesome icon="edit" /></Link>
								<Link onClick={::this.trash} className="btn btn-danger btn-sm" title="Delete"><FontAwesome icon="trash" /></Link>
							</div>
						</div>
					</div>
				</div>
				<div className="box-body">
					<dl className="dl-horizontal">
						{Object.entries({
							name: 'Name',
							active: 'Active',
						}).map(
							([ key, name ]) => (
								<div key={key}>
									<dt>{name}</dt>
									<dd>{String(vat[key])}</dd>
								</div>
							)
						)}
						<div>
							<dt>Known VAT Periods</dt>
							<dd>
								{
									vat.vatperiod_set.length > 0 ? (
										<table className="table table-striped">
											<thead>
												<tr>
													<th>Begin date</th>
													<th>End date</th>
													<th>Rate (* factor)</th>
												</tr>
											</thead>
											<tbody>
												{
													vat.vatperiod_set.map(
														period => (
															<tr key={period.id}>
																<td>{period.begin_date}</td>
																<td>{period.end_date || '< NONE >'}</td>
																<td>{period.vatrate}</td>
															</tr>
														)
													)
												}
											</tbody>
										</table>
									) : 'none'
								}
							</dd>
						</div>
					</dl>
				</div>
			</div>
		);
	}
}

export default connect(
	(state, props) => ({ VAT: (state.VATs.VATs || []).find(el => +el.id === +props.params.VATID) })
)(VATDetail);
