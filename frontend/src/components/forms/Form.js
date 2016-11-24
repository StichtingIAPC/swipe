import React, { PropTypes } from 'react';
import { Link } from 'react-router';

import FA from '../tools/FontAwesome';

/**
 * Created by Matthias on 18/11/2016.
 */

export class Form extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			local: this.props.original,
			working_copy: {...this.props.original},
		};
	}

	reset(evt) {
		this.setState({working_copy: {...this.props.original}});
	}


	onSubmit(evt) {
		evt.preventDefault();
		this.props.onSubmit(this.state.working_copy);
	}

	updateValues(key, value) {
		const working_copy = {...this.state.working_copy};
		working_copy[key] = value;
		this.setState({working_copy: working_copy})
	}

	componentWillReceiveProps(nextProps) {
		if (this.state.local != nextProps.original) {
			this.setState({
				local: nextProps.original,
				working_copy: {...nextProps.original},
			});
		}
	}

	render() {
		const update_value = (key) => ((evt) => this.updateValues(key, evt.target.value));

		return (
			<div className="box">
				<div className="box-header with-border">
					{this.props.children}
					<div className="box-tools">
						<div className="input-group">
							<div className="btn-group">
								<Link to={this.props.returnLink} className="btn btn-default btn-sm" title="Close"><FA icon="close" /></Link>
								<Link onClick={this.reset.bind(this)} className="btn btn-warning btn-sm" title="Reset"><FA icon="repeat" /></Link>
							</div>
						</div>
					</div>
				</div>
				<div className="box-body">
					<form className="form-horizontal" onSubmit={this.onSubmit.bind(this)} >
						{Object.keys(this.props.fields).map(
							(key) => {
								const Input = this.props.fields[key];
								return (
									<div key={key} className="form-group">
										<label className="col-sm-2 control-label">{key}</label>
										<div className="col-sm-10">
											<Input onChange={update_value(key)} value={this.state.working_copy[key] || ""} />
										</div>
									</div>
								)
							}
						)}
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
	fields: PropTypes.objectOf(
		PropTypes.func.isRequired
		// All React Components are functions, and therefore are validated here.
		// see https://github.com/facebook/react/issues/5143 for explanation why this is the least worst solution
	).isRequired,
	children: PropTypes.node.isRequired,
	returnLink: PropTypes.string.isRequired,
	original: PropTypes.object.isRequired,
};

Form.defaultProps = {
	original: {},
};

export default Form;
