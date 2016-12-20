import React, { PropTypes } from "react";
import { Link } from "react-router";
import FontAwesome from "../tools/icons/FontAwesome";

export default class Form extends React.Component {
	render() {
		return (
			<div className={`box${this.props.error ? ' box-danger box-solid' : ''}`}>
				<div className="box-header with-border">
					<h3 className="box-title">{this.props.title}</h3>
					<div className="box-tools">
						<div className="input-group">
							<div className="btn-group">
								{
									this.props.closeLink ? (
										<Link to={this.props.closeLink} className="btn btn-default btn-sm" title="Close"><FontAwesome icon="close" /></Link>
									) : null}
								<Link to={this.props.returnLink} className="btn btn-default btn-sm" title="Return"><FontAwesome icon="arrow-left" /></Link>
								<Link onClick={this.props.onReset} className="btn btn-warning btn-sm" title="Reset"><FontAwesome icon="repeat" /></Link>
							</div>
						</div>
					</div>
				</div>
				<div className="box-body">
					<form className="form-horizontal" onSubmit={this.props.onSubmit} >
						{this.props.children}
						<div className="form-group">
							<div className="col-sm-9 col-sm-offset-3">
								<button className="btn btn-success">Save</button>
							</div>
						</div>
					</form>
				</div>
				{
					this.props.error ? (
						<div className="box-footer">
							<FontAwesome icon="warning" />
							<span>{JSON.stringify(this.props.error)}</span>
						</div>
					) : null
				}
			</div>
		)
	}
}

Form.propTypes = {
	children: PropTypes.node.isRequired,
	returnLink: PropTypes.string.isRequired,
	closeLink: PropTypes.string,
	title: PropTypes.string.isRequired,
	onReset: PropTypes.func.isRequired,
	onSubmit: PropTypes.func.isRequired,
	error: PropTypes.string,
};

Form.defaultProps = {
	returnLink: '/',
};
