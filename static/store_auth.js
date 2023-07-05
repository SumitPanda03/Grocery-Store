// Perform login and store the token in local storage
function login() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
  
    // Make a POST request to the Flask API for login
    axios.post('/login', { username: username, password: password })
      .then(function(response) {
        // Retrieve the token from the response
        var token = response.data.token;
        
        // Store the token in the local storage
        localStorage.setItem('token', token);
  
        // Redirect to the desired page or perform other actions
        window.location.href = '/dashboard';
      })
      .catch(function(error) {
        // Handle login error
        console.error(error);
      });
  }
  