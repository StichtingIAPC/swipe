import React from 'react';
import { Link } from 'react-router'

/**
 * Created by Matthias on 08/11/2016.
 */

export class Error404 extends React.Component {
  render() {

    return <div className="small-10 small-offset-1 medium-8 medium-offset-2 large-6 large-offset-3">
      <div className="card">
        <h1>Error 404</h1>
        <p>Route not found.</p>
        <p>
          Click to return to the <Link to="/dashboard">dashboard</Link>
        </p>
      </div>
    </div>
  }
}