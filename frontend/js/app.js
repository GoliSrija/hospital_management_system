
        const loginForm =
        document.getElementById("loginForm");

        if(loginForm){

        loginForm.addEventListener(
        "submit",
        function(e){

        e.preventDefault();

        window.location.href =
        "dashboard.html";

        });

        }

        const registerForm =
        document.getElementById("registerForm");

        if(registerForm){

        registerForm.addEventListener(
        "submit",
        function(e){

        e.preventDefault();

        window.location.href =
        "login.html";

        });

        }
        