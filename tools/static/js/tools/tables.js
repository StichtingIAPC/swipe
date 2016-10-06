/**
 * @callback lookup
 * @param {Row} row
 * @returns {T}
 * @template T
 */

/**
 * @typedef {Iterable<Row>} Dataprovider
 */

/**
 * @typedef {(Array|Object)} Row
 */

export class Table {
  /**
   * The js alternative to the python tools.tables.Table class
   *
   * @param {Array<Column>} columns
   * @param {Dataprovider} dataprovider: the iterator which results in the
   * data which is put into the table.
   * @param {Array<String>} classes: the CSS classes to give to the table.
   * @param {Object} extras: This is an extra field for js, to attach extra callbacks to the whole table.
   *
   * NOTE that the extras are only added to the table, and can therefore not directly be used as a way to
   * get data out of the table. If you want that, you can subclass Table and provide your own RowRenderer/
   * render methods.
   */
  constructor(columns, dataprovider, classes, extras) {
    this.columns = columns;
    this.data = [...dataprovider];
    this.classes = classes;
    this.extras = extras;
  }

  render(emit, refresh) {
    let self = this;

    function render(tbl) {
      `
      <table class="{{ self.classes.join(' ') }}" {{ self.extras }}>
        <thead>
          <tr>
          {% for col in self.columns %}{{col.HeadRenderer}}{% endfor %}
          </tr>
        </thead>
        <tbody>
          {% for row in self.rows %}
          {% include self.RowRenderer with row=row %}{% endfor %}
        </tbody>
      </table>
      `;
      return [
        'table', Object.assign(
          { class: self.classes.join(' ')},
          self.extras
        ),
        [
          'thead', {

          },
          [ 'tr', {},
            self.columns.map((col) => [col.HeaderRenderer])
          ]
        ],
        [
          'tbody', {
          },
          self.data.map(
            /**
             * @param {Row} row
             */
            (row) => [self.RowRenderer, row]
          )
        ]
      ];
    }

    return {
      render: render
    };
  }

  /**
   * @param {Emit} emit
   * @param {Refresh} refresh
   */
  RowRenderer(emit, refresh) {
    let self = this;
    function render(row) {
      `
      <tr>{% for col in self.columns %}
        {% include col.CellRenderer with value=column.key(row) %}{% endfor %}
      </tr>
      `;
      return [
        'tr', {},
        self.columns.map((column) => [column.CellRenderer, column.key(row)])
      ];
    }
  }
}

export class Column {
  /**
   * The base class for any columns in the Table. Please extend this class, and override the
   * CellRenderer and HeadRenderer methods when needed.
   *
   * @param {lookup} key
   * @param name
   */
  constructor(key, name) {
    this.name = name ? name : "Column";
    this.key = key;
  }

  /**
   * @returns {{render: render}}
   * @constructor
   */
  CellRenderer() {
    let self = this;

    /**
     * @returns {*[]}
     */
    function render(cell_value) {
      return [
        'td', {
        },
        cell_value
      ];
    }
    return {
      render: render
    };
  }

  /**
   * @returns {{render: render}}
   * @constructor
   */
  HeaderRenderer() {
    let self = this;

    /**
     * @returns {*[]}
     */
    function render() {
      return [
        'td', {},
        self.name
      ];
    }
    return {
      render: render
    };
  }
}