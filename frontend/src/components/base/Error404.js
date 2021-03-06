import React from 'react';
import { Link } from 'react-router-dom';

export class Error404 extends React.Component {
	render() {
		return (
			<div className="row">
				<div className="col-sm-10 col-sm-offset-1 col-md-8 col-sm-offset-2 col-md-6 col-md-offset-3">
					<div className="box box-danger">
						<div className="box-header with-border">
							<h3>Error 404</h3>
						</div>
						<div className="box-body">
							<p>
								Route not found.
							</p>
							<p>
								Click to return to the <Link to="/dashboard">dashboard</Link>
							</p>
						</div>
					</div>
				</div>
			</div>
		);
	}
}
