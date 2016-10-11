/**
 * Created by Matthias on 11/10/2016.
 */

import { Column } from 'js/tools/tables'



class ProductLabelsColumn extends Column {
  CellRenderer() {
    let self = this;

    /**
     * @returns {*[]}
     */
    function render(labels) {
      return [
        'td', {
        },
        labels.map((label) => [[
          'span', {},
          label
        ], ' '])
      ];
    }
    return {
      render: render
    };
  }
}
