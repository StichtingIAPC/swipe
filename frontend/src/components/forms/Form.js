import React from 'react';
import PropTypes from 'prop-types';
import {Link} from 'react-router-dom';
import FontAwesome from '../tools/icons/FontAwesome';
import Box from "../base/Box";

export default class Form extends React.Component {
	onSubmit = evt => {
		evt.preventDefault();
		return this.props.onSubmit(evt);
	};

	render() {
		return (
			<Box error={this.props.error}>
				<Box.Header
					title={this.props.title}
					buttons={
						<React.Fragment>
							{
								this.props.returnLink ?
									<Link
										to={this.props.returnLink}
										className="btn btn-default btn-sm"
										title="Return">
										<FontAwesome
											icon="arrow-left"/>
									</Link> : null
							}
							<a
								onClick={this.props.onReset}
								className="btn btn-warning btn-sm"
								title="Reset">
								<FontAwesome icon="repeat" />
							</a>
							{
								this.props.closeLink ? (
									<Link
										to={this.props.closeLink}
										className="btn btn-default btn-sm"
										title="Close"><FontAwesome icon="close"/></Link>
								) : null
							}
						</React.Fragment>
					}/>
				<Box.Body>
					<form className="form-horizontal" onSubmit={this.onSubmit}>
						<div className="col-sm-12">
							{this.props.children}
						</div>
						<div className="form-group">
							<div className="col-sm-9 col-sm-offset-3">
								<button className="btn btn-success" disabled={this.props.disabled}>Save</button>
							</div>
						</div>
					</form>
				</Box.Body>
				{
					this.props.error ? (
						<Box.Footer>
							<FontAwesome icon="warning"/>
							<span>{JSON.stringify(this.props.error)}</span>
						</Box.Footer>
					) : null
				}
			</Box>
		);
	}
}

Form.propTypes = {
	children: PropTypes.node.isRequired,
	returnLink: PropTypes.string,
	closeLink: PropTypes.string,
	title: PropTypes.string.isRequired,
	onReset: PropTypes.func.isRequired,
	onSubmit: PropTypes.func.isRequired,
	error: PropTypes.string,
	disabled: PropTypes.bool,
};
