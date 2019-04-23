"use strict";
(function(_d, _w, _t, _s){
  var web = {
    getCookie : function (name) {  
      var matches = _d.cookie.match(new RegExp(name + '=([^;]+)'));
      if (matches) return matches[1];
      return
    },
    authLoad : function(){ 
      _t = this;
      _w.addEventListener('load', function() {
        var idToken;
        var accessToken;
        var expiresAt;
      
        var authOpt = {
          domain: __web.auth_domain,
          clientID: __web.auth_id
        }
  
        Object.assign(authOpt,
          {
            responseType: 'token id_token',
            scope: 'email',
            redirectUri: _w.location.href + 'callback/auth'
          }
        )
  
        var webAuth = new auth0.WebAuth(authOpt);
      
        var loginBtn = _d.getElementById('btn-login');
      
        loginBtn.addEventListener('click', function(e) {
          e.preventDefault();
          webAuth.authorize();
        });
      
      });
    }
  }
  var app = new Vue({
    el: '#app',
    mounted: function(){
      if(typeof __web != 'undefined' && __web.auth_domain){
        web.authLoad();
      }
    },
    data: {
      message: 'Hello!',
      fields: [
      ],
      items: [
      ]
    }
  })
})(document, window, {}, {});


