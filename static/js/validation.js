

        var username = document.getElementById('username');
        var password = document.getElementById('password');
        var confirmPassword = document.getElementById('confirmPassword');
        var form = document.getElementById('form');

        form.addEventListener('submit', (e) => {
        let message = []
        if (username.length <= 5 || username.value >= 20){
            message.push('Name cannot be less than 5 and more than 20 characters')

        if ( password.value != confirmPassword.value ){}
            message.push('Passwords do not match')
        }

        if (message.length > 0){
        e.preventDefault()
        errorElement.innerText = messages.join(' , ')
        }
        }

