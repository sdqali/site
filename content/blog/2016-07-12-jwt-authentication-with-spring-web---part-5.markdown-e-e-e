---
Categories:
- development
- java
- spring
- jwt
- spring security
Description: ""
Tags:
- development
- java
- spring
- jwt
- spring security
series:
- spring-jwt
date: 2016-07-13T23:05:53-07:00
image: "images/jwt.jpg"
title: JWT authentication with Spring Web - Part 5
---
In parts 1 through 4 of this series, we built a Spring API that can issue a JWT when a user successfully authenticates and verify the JWT presented by the client for subsequent requests. In this blog post - the last in the series, we will build a simple Angular JS application with authentication that uses this API as the backend.
<!--more-->
These are the blog posts in this series:

* [Part 1](/blog/2016/07/02/jwt-authentication-with-spring-web---part-1/) - Discussion of JWT and implementation
* [Part 2](/blog/2016/07/03/jwt-authentication-with-spring-web---part-2/) - A Spring User Profiles API
* [Part 3](/blog/2016/07/05/jwt-authentication-with-spring-web---part-3/) - Issuing a token from the server
* [Part 4](/blog/2016/07/07/jwt-authentication-with-spring-web---part-4/) - Verifying the token sent back by the client
* [Part 5](/blog/2016/07/13/jwt-authentication-with-spring-web---part-5/) - Securing the front end

We will use the following Angular plugins - `angular-resource` for interacting with our APIs, `ngstorage` to access the localStorage to store the JWT and `angular-ui-router` to handle routing and managing UI views.

For this example, our UI components are under the `src/main/resources/static` directory. We will be loading our dependencies using bower by adding a `.bowerrc` file at the root of our project.

```json
{
  "directory": "src/main/resources/static/bower_components",
  "json": "bower.json"
}
```

We will specify the dependencies we need in our `bower.json`:

```json
{
  "name": "jwt",
  "dependencies": {
    "angular": "~1.3.0",
    "angular-resource": "~1.3.0",
    "bootstrap-css-only": "~3.2.0",
    "ngstorage": "0.3.10",
    "angular-ui-router": "1.0.0-beta.1"
  }
}
```

The dependencies can be installed using `bower install`. Once we have the dependencies, we can start by configuring Spring Security to allow access to the UI components:

```java
        String[] patterns = new String[] {
            "/login",
            "/bower_components/**/*",
            "/app/**/*",
            "/index.html",
            "/home.html",
            "/signin.html"
        };
        http.authorizeRequests()
                .antMatchers(patterns)
                .permitAll()
        // ...
```

We will start by creating our UI template `index.html`:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <link rel="stylesheet" href="./bower_components/bootstrap-css-only/css/bootstrap.min.css" />
  </head>
  <body ng-app="jwtDemo">
    <div class="container">
      <ui-view></ui-view>
    </div>
    <script type="text/javascript" src="./bower_components/angular/angular.min.js"></script>
    <script type="text/javascript" src="./bower_components/angular-resource/angular-resource.min.js"></script>
    <script type="text/javascript" src="./bower_components/ngstorage/ngStorage.min.js"></script>
    <script type="text/javascript" src="./bower_components/angular-ui-router/release/angular-ui-router.min.js"></script>
    <script type="text/javascript" src="./app/app.js"></script>
    <script type="text/javascript" src="./app/controllers.js"></script>
    <script type="text/javascript" src="./app/services.js"></script>
  </body>
</html>
```

For this example, we will have one Angular service in `app/services.js` that performs login:

```javascript
(function(angular) {
  var LoginFactory = function($resource) {
    return $resource('/login', {}, {
      login: {
        method: 'POST'
      }
    });
  };

  LoginFactory.$inject = ['$resource'];
  angular.module('jwtDemo.services').factory('Login', LoginFactory);
}(angular));
```

We will need two controllers in `app/controller.js` - one for the login page to manage login and one for the profile page:

```javascript
(function(angular) {
  var LoginController = function($scope, $localStorage, $http, $location, Login) {
    $scope.login = function(username, password) {
      new Login({username: username, password: password})
          .$login(function (profile, headers) {
            $localStorage.user = profile;
            $localStorage.token = headers().token;
            $http.defaults.headers.common.Authorization = 'Bearer ' + headers().token;
            $location.path("/");
          }, function (error) {
            console.log(error);
          });
    };

    $scope.logout = function () {
      delete $localStorage.user;
      delete $localStorage.token;
      $http.defaults.headers.common = {};
    }

    $scope.logout();
  };

  LoginController.$inject = ['$scope', '$localStorage', '$http', '$location','Login'];
  angular.module("jwtDemo.controllers").controller("LoginController", LoginController);


  var ProfileController = function ($scope, $localStorage) {
    $scope.profile = $localStorage.user;
  };
  ProfileController.inject = ['$scope', '$localStorage'];
  angular.module("jwtDemo.controllers").controller("ProfileController", ProfileController);
}(angular));
```

The `LoginController` has two methods - login and logout. The login method uses the `LoginService` to make a request and saves the JWT and user profile returned up on successful login. It also sets the `Authorization` header default to the JWT returned so that every subsequent request uses it to authenticate. The user is then navigated to the home page. Logout is performed by removing the JWT and profile from local storage and clearing the header defaults.

The next step is to create `app/app.js` to wire up the Angular application together:

```javascript
(function(angular) {
  angular.module("jwtDemo.controllers", []);
  angular.module("jwtDemo.services", []);
  angular.module("jwtDemo", ["ui.router", "ngResource", "ngStorage", "jwtDemo.controllers", "jwtDemo.services"])
      .config(function ($stateProvider, $urlRouterProvider) {
        $urlRouterProvider.otherwise("/");

        $stateProvider
            .state('home', {
              url: '/',
              templateUrl: 'home.html',
              controller: 'ProfileController'
            })
            .state('signin', {
              url: '/signin',
              templateUrl: 'signin.html',
              controller: 'LoginController'
            })
            .state('signout', {
              url: '/signout',
              templateUrl: 'signin.html',
              controller: 'LoginController'
            });
      })
      .run(function ($localStorage, $http, $location, $rootScope) {
        if ($localStorage.user) {
          $http.defaults.headers.common.Authorization = 'Bearer ' + $localStorage.token;
        }

        $rootScope.$on('$locationChangeStart', function (event, next, current) {
          if ($location.path() !== "/signin" && !$localStorage.user) {
            $location.path('/signin');
          } else if ($location.path() === "/signin" && $localStorage.user) {
            $location.path('/');
          }
        });
      });
}(angular));
```

We start by wiring together our services and controllers to the main module. We use the state provider to map front end URLs to templates. The home page will use the `home.html` template and the sign in and sign out URLs will use the `sigin.html` template.

It also configures a listener that observes for URL changes made by the user and redirects them to the sign in page, unless they are already authenticated. If there is already a token in local storage when the application loads, that signifies that the user has already logged in a different tab and the authorization header default is set.

The two views we have are simple - `signin.html` has a sign form:
```html
<div class="row">
  <div class='col-md-3'></div>
  <div class="col-md-6">
    <div class="login-box well">
      <form role="form" ng-submit="login(username, password)">
        <legend>Sign In</legend>
        <div class="form-group">
          <label for="username-email">Username</label>
          <input ng-model="username" value='' id="username-email" placeholder="Username" type="text"
                 class="form-control" />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input ng-model="password" id="password" value='' placeholder="Password" type="password"
                 class="form-control" />
        </div>
        <div class="form-group">
          <input type="submit" class="btn btn-default btn-login-submit btn-block m-t-md" value="Login" />
        </div>
      </form>
    </div>
  </div>
  <div class='col-md-3'></div>
</div>
```

The view for home page - `home.html` renders a user profile:

```html
<div class="row">
  <h1>Welcome, {{profile.name.first}}</h1>
  <div class="col-lg-3 col-sm-6">
    <div class="card hovercard">
      <div class="cardheader">
      </div>
      <div class="avatar">
        <img alt="" src="{{profile.thumbnail}}">
      </div>
      <div class="info">
        <div class="title">
          {{profile.username}}
        </div>
        <div class="desc">{{profile.name.first}} {{profile.name.last}}</div>
      </div>
      <div>
        <a href="/#/signout">Sign Out</a>
      </div>
    </div>
  </div>
</div>
```
It also has a link for signing out. With this code in place, we can start our Spring application and sign in from the browser.

This is the last of this series of blog posts on JWT and Spring. We built an API capable of authenticating with JWTs and a front end capable of authenticating against this API. The code for the complete example is available on [GitHub](https://github.com/sdqali/jwt-demo).
