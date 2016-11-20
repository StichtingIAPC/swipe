import React from 'react';
import {Link} from 'react-router';
import { connect } from 'react-redux';

import FA from 'tools/components/FontAwesome';

/**
 * Created by Matthias on 17/11/2016.
 */

let SupplierList = class extends React.Component {
	render() {
		return (
			<div className="box">
				<div className="box-header with-border">
					<h3 className="box-title">Supplier list</h3>
					<div className="box-tools">
						<div className="input-group">
							<div className="btn-group">
								<Link className="btn btn-default btn-sm" to="/supplier/create/" title="Create new supplier"><FA icon="plus" /></Link>
							</div>
						</div>
					</div>
				</div>
				<div className="box-body">
					<table className="table table-striped">
						<thead>
							<tr>
								<th>
									<span>Supplier Name</span>
								</th>
								<th>
									<span className="pull-right">Options</span>
								</th>
							</tr>
						</thead>
						<tbody>
							{Object.keys(this.props.suppliers).filter((key) => this.props.suppliers[key]).map(
								(id) => (
									<tr key={id} className={Number(this.props.supplierID) == id ? 'active' : null}>
										<td>
											{this.props.suppliers[id].name}
										</td>
										<td>
											<div className="btn-group pull-right">
												<Link to={`/supplier/${id}/`} className="btn btn-default btn-xs" title="Details">
													<FA icon="crosshairs" />
												</Link>
												<Link to={`/supplier/${id}/edit/`} className="btn btn-default btn-xs" title="Edit">
													<FA icon="edit" />
												</Link>
											</div>
										</td>
									</tr>
								)
							)}
						</tbody>
					</table>
				</div>
			</div>
		)
	}
};

SupplierList.defaultProps = {
	suppliers: {
		1: {
			name: 'Nedis',
			id: 1,
		},
		2: {
			name: 'Copaco',
			id: 2,
		},
	},
};

SupplierList = connect(
	(state, ownProps) => {
		console.log(state);
		return {
			...ownProps,
			suppliers: state.suppliers.objects,
		}
	})(SupplierList);

export {
	SupplierList,
};
export default SupplierList;
