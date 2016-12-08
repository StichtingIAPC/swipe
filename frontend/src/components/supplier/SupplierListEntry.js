import React from 'react';
import { Link } from 'react-router';

import FontAwesome from '../tools/icons/FontAwesome';

export default class SupplierListEntry extends React.Component {
	render() {
		return (
			<tr className={Number(this.props.supplierID) == this.props.supplier.id ? 'active' : null}>
				<td>
					{this.props.supplier.name}
				</td>
				<td>
					<div className="btn-group pull-right">
						{
							this.props.supplier.updating ? (
								<Link
									to="#"
									className="btn btn-success btn-xs disabled"
									title="Updating">
									<FontAwesome icon="refresh" />
								</Link>
							) : null
						}
						<Link
							to={`/supplier/${this.props.supplier.id}/`}
							className="btn btn-default btn-xs"
							title="Details">
							<FontAwesome icon="crosshairs" />
						</Link>
						<Link
							to={`/supplier/${this.props.supplier.id}/edit/`}
							className="btn btn-default btn-xs"
							title="Edit">
							<FontAwesome icon="edit" />
						</Link>
					</div>
				</td>
			</tr>
		)
	}
}
