import React from 'react';

/**
 * Created by Matthias on 16/11/2016.
 */

export default class FontAwesome extends React.Component {
  render() {
    return (
      <i className={`fa fa-${this.props.icon}`}/>
    )
  }
}
