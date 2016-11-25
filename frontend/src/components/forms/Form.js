import React, { PropTypes } from 'react';
import { Link } from 'react-router';

import FA from '../tools/FontAwesome';

/**
 * Created by Matthias on 18/11/2016.
 */

export class Form extends React.Component {
	render() {
		return (
			<div className="box">
				<div className="box-header with-border">
					<h3 className="box-title">{this.props.title}</h3>
					<div className="box-tools">
						<div className="input-group">
							<div className="btn-group">
								<Link to={this.props.returnLink} className="btn btn-default btn-sm" title="Close"><FA icon="close" /></Link>
								<Link onClick={this.props.onReset} className="btn btn-warning btn-sm" title="Reset"><FA icon="repeat" /></Link>
							</div>
						</div>
					</div>
				</div>
				<div className="box-body">
					<form className="form-horizontal" onSubmit={this.props.onSubmit} >
						{this.props.children}
						<div className="form-group">
							<div className="col-sm-10 col-sm-offset-2">
								<button className="btn btn-success">Save</button>
							</div>
						</div>
					</form>
				</div>
			</div>
		)
	}
}

Form.propTypes = {
	children: PropTypes.node.isRequired,
	returnLink: PropTypes.string.isRequired,
	title: PropTypes.string.isRequired,
	onReset: PropTypes.func.isRequired,
	onSubmit: PropTypes.func.isRequired,
};

Form.defaultProps = {
	returnLink: '/',
};

export default Form;
