require.config({
  baseURL: "static/js",
  paths: {
    axios: "../build/bower_components/axios/dist",
    domchanger: "../build/bower_components/domchanger",
    mini_signals: "../build/bower_components/mini-signals"
  }
});

requirejs([
  'axios/axios',
  'domchanger/domchanger',
  'mini_signals/browser',
  'main'
]);