import React from 'react';

export default class Box extends React.Component {
	static Header = ({ title, buttons, withBorder }) => (
		<div className={`box-header${withBorder ? ' with-border' : ''}`}>
			<div className="box-title">{title}</div>
			<div className="box-tools">
				<div className="input-group">
					<div className="btn-group">
						{buttons}
					</div>
				</div>
			</div>
		</div>
	);

	static Body = ({ children }) => (
		<div className="box-body">{children}</div>
	);

	static Footer = ({ children }) => (
		<div className="box-body">{ children }</div>
	);

	constructor(props) {
		super(props);
		this.state = {
			err: false,
		};
	}

	componentWillCatch(err) {
		console.log(err);
		this.setState(() => ({ err: true }));
	}

	render() {
		if (this.state.err) {
			return (
				<div className="box">
					<this.Header title="Error in this component" />
				</div>
			);
		}

		return (
			<div className="box">
				{ this.props.children }
			</div>
		);
	}
}
