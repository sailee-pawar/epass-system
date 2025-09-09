
// Checks session validity every 60 seconds and redirects to login if session expired
setInterval(function() {
    fetch('/dashboard/', { method: 'GET', credentials: 'same-origin' })
        .then(function(response) {
            if (response.redirected) {
                window.location.href = response.url;
            } else if (response.status === 401) {
                window.location.href = '/login/';
            }
        })
        .catch(function(error) {
            // Optionally handle network errors
        });
}, 60000); // 60,000 ms = 60 seconds
