import React from 'react';
import autoBind from 'react-autobind';
import { connect } from 'react-redux';
import auth from '../../../core/auth';
import { failAuthentication } from '../../../actions/auth';
import { AUTHENTICATING } from '../../../reducers/auth';
import Glyph from 'tools/components/Glyphicon';

/**
 * Created by Matthias on 18/11/2016.
 */

let LoginModal = class extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			username: '',
			password: '',
		};
		autoBind(this);
	}
	cancel() {
		auth.cancel();
	}

	async accept() {
		auth.login({
			username: this.state.username,
			password: this.state.password,
		});
	}

	render() {
		const setValue = (str) =>
			(evt) =>
				this.setState({[str]: evt.target.value });
		if (this.props.status == AUTHENTICATING) {
			return (
				<div className="modal modal-warning" tabIndex="-1" style={{display: 'block'}}>
					<div className="modal-dialog modal-sm">
						<div className="modal-content">
							<div className="modal-header">
								<button className="close" onClick={this.cancel.bind(this)}>
									<Glyph glyph="remove" />
								</button>
								<h4 className="modal-title">Please provide valid credentials before continuing.</h4>
							</div>
							<div className="modal-body">
								<form onSubmit={this.accept.bind(this)} className="">
									<div className="form-group has-feedback">
										<input
											className="form-control"
											type="text"
											value={this.state.username}
											onChange={setValue('username')} />
										<Glyph glyph="user form-control-feedback" />
									</div>
									<div className="form-group has-feedback">
										<input
											className="form-control"
											type="password"
											value={this.state.password}
											onChange={setValue('password')} />
										<Glyph glyph="lock form-control-feedback" />
									</div>
								</form>
							</div>
							<div className="modal-footer">
								<button className="btn btn-outline pull-left" onClick={this.cancel.bind(this)}>Cancel</button>
								<button className="btn btn-outline" onClick={this.accept.bind(this)}>Login</button>
							</div>
						</div>
					</div>
				</div>
			)
		} else {
			return null;
		}
	}
};

LoginModal.propTypes = {

};

LoginModal = connect(
	(state, ownProps) => {
		return {
			...ownProps,
			status: state.auth.status,
		}
	}
)(LoginModal);

export {
	LoginModal,
};

export default LoginModal;
