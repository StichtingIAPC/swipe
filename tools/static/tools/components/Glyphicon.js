import React from 'react';

/**
 * Created by Matthias on 06/11/2016.
 */

export default class Glyphicon extends React.Component {
	render() {
		return (
			<span onClick={this.props.onClick}
						className={`glyphicon glyphicon-${this.props.glyph} ${this.props['x-class']}`}></span>
		)
	}
}
