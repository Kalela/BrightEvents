var Router = ReactRouter.Router;
var Route = ReactRouter.Route;
var browserHistory = ReactRouter.browserHistory

ReactDOM.render((
  <Router history={browserHistory}>
    <Route path="/" component={Index} />
  </Router>
  ),
  document.getElementById('container')
);