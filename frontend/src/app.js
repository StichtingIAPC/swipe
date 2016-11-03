'use strict';

import React from 'react';
import ReactDOM from 'react-dom';

class Application extends React.Component {
	render() {
		return <span>Hello world</span>;
	}
}

ReactDOM.render(<Application />, document.getElementById('app'));