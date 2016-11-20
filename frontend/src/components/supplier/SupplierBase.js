import React from 'react';
import { connect } from 'react-redux'

import SupplierList from './SupplierList';

/**
 * Created by Matthias on 17/11/2016.
 */

export class SupplierBase extends React.Component {
	render() {
		return (
			<div className="row">
				<div className="col-xs-6 col-md-6">
					<SupplierList supplierID={this.props.params.supplierID || ''} />
				</div>
				<div className="col-xs-6 col-md-6">
					{this.props.children}
				</div>
			</div>
		)
	}
}

export default SupplierBase;
