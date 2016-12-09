import React from 'react';

export default class Glyphicon extends React.Component {
	render() {
		return <span
			onClick={this.props.onClick}
			className={`glyphicon glyphicon-${this.props.glyph} ${this.props['x-class']}`} />;
	}
}
