import React from 'react';
import {Link} from 'react-router';
import { connect } from 'react-redux';

import FA from '../tools/FontAwesome';

import SupplierListEntry from './SupplierListEntry';

import { populateSuppliers } from '../../actions/suppliers';

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
								<Link
									className={`btn btn-sm ${this.props.invalid ? 'btn-danger' : 'btn-default'} ${this.props.fetching ? 'disabled' : ''}`}
									to="#"
									title="Refresh"
									onClick={this.props.update}>
									<FA icon={`refresh ${this.props.fetching ? 'fa-spin' : ''}`} />
								</Link>
								<Link
									className="btn btn-default btn-sm"
									to="/supplier/create/"
									title="Create new supplier">
									<FA icon="plus" />
								</Link>
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
									<SupplierListEntry supplierID={this.props.supplierID} key={id} supplier={this.props.suppliers[id]} />
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
		return {
			...ownProps,
			suppliers: state.suppliers.objects,
			invalid: state.suppliers.invalid,
			fetching: state.suppliers.fetching,
		}
	},
	(dispatch, ownProps) => {
		return {
			...ownProps,
			update: (evt) => {
				evt.preventDefault();
				dispatch(populateSuppliers());
			},
		}
	})(SupplierList);

export {
	SupplierList,
};
export default SupplierList;
