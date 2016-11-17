/**
 * Created by Matthias on 11/10/2016.
 */

import { Column } from 'js/tools/tables'



export class ProductLabelsColumn extends Column {
  constructor() {
    super();

    this.CellRenderer = class extends React.Component {
      render() {
        const labels = this.props['labels'].map((label) =>
          <span key={label}>{label}</span>
        );
        return <td>{ labels }</td>
      }
    }
  }
}
