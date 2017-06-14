import React from 'react';

export default function Step({ name, children, summary, active }) {
	return <div className="box step">
		<header className="step-header">
			<h2>{name}</h2>
			<div className="summary">{active ? '' : summary}</div>
		</header>
		<div>{active ? children : ''}</div>
	</div>;
}
