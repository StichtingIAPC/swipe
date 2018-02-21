import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import FontAwesome from '../../../tools/icons/FontAwesome';
import Box from '../../../base/Box';

class VATDetail extends React.Component {
	static propTypes = {
		vat: PropTypes.shape({
			id: PropTypes.number,
			name: PropTypes.string.isRequired,
			active: PropTypes.bool.isRequired,
			vatperiod_set: PropTypes.arrayOf(PropTypes.number).isRequired,
		}),
	};

	trash = () => null;

	render() {
		const { vat } = this.props;

		return (
			<Box>
				<Box.Header
					title={`VAT: ${vat.name}`}
					buttons={
						<React.Fragment>
							<Link to={`/money/vat/${vat.id}/edit/`} className="btn btn-default btn-sm" title="Edit"><FontAwesome icon="edit" /></Link>
							<a onClick={this.trash} className="btn btn-danger btn-sm" title="Delete"><FontAwesome icon="trash" /></a>
						</React.Fragment>
					} />
				<Box.Body>
					<dl className="dl-horizontal">
						{Object.entries({
							name: 'Name',
							active: 'Active',
						}).map(
							([ key, name ]) => (
								<React.Fragment key={key}>
									<dt>{name}</dt>
									<dd>{String(vat[key])}</dd>
								</React.Fragment>
							)
						)}
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
					</dl>
				</Box.Body>
			</Box>
		);
	}
}

export default connect(
	state => ({
		vat: state.money.vats.activeObject,
	})
)(VATDetail);
