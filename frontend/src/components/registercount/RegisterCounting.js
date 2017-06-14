import React from 'react';
export default class RegisterCounting extends React.Component {
	render() {
		return (
			<div className="col">
				{this.props.children && React.Children.only(this.props.children)}
			</div>
		);
	}
}
