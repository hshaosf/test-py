var app = new Vue({
    el: '#app',
    data: {
      message: 'Hello!',
      fields: [
      ],
      items: [
      ]
    }
  })

var web = {
  auth_load : function(){
    window.addEventListener('load', function() {
      var idToken;
      var accessToken;
      var expiresAt;
    
      var authOpt = {
        domain: '',
        clientID: ''
      }

      Object.assign(authOpt,
        {
          responseType: 'token id_token',
          scope: 'email',
          redirectUri: window.location.href + 'callback/auth'
        }
      )

      var webAuth = new auth0.WebAuth(authOpt);
    
      var loginBtn = document.getElementById('btn-login');
    
      loginBtn.addEventListener('click', function(e) {
        e.preventDefault();
        webAuth.authorize();
      });
    
    });
  }
}