(() => {
    "use strict";

    const apiBase = String(
        (window.APP_CONFIG || {}).API_BASE_URL || ""
    ).replace(/\/+$/, "");

    async function api(path, options = {}) {
        if (!apiBase) {
            throw new Error("API_BASE_URL is missing in js/config.js.");
        }

        const response = await fetch(apiBase + path, {
            credentials: "include",
            ...options,
            headers: {
                "Content-Type": "application/json",
                ...(options.headers || {})
            }
        });

        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            throw new Error(data.message || "Request failed.");
        }

        return data;
    }

    function showMessage(form, text, isError = false) {
        let node = form.querySelector(".status-message");

        if (!node) {
            node = document.createElement("p");
            node.className = "status-message";
            node.setAttribute("role", "status");
            form.prepend(node);
        }

        node.textContent = text;
        node.classList.toggle("status-error", isError);
    }

    document.addEventListener("DOMContentLoaded", () => {
        const loginForm = document.getElementById("loginForm");

        if (loginForm) {
            loginForm.addEventListener("submit", async event => {
                event.preventDefault();

                const button = loginForm.querySelector(
                    'button[type="submit"]'
                );

                if (button) button.disabled = true;

                try {
                    const email = loginForm
                        .querySelector('[name="email"]').value.trim();

                    const password = loginForm
                        .querySelector('[name="password"]').value;

                    await api("/api/auth/login", {
                        method: "POST",
                        body: JSON.stringify({ email, password })
                    });

                    window.location.href = "dashboard.html";
                } catch (error) {
                    showMessage(
                        loginForm,
                        error.message || "Login failed.",
                        true
                    );
                } finally {
                    if (button) button.disabled = false;
                }
            });
        }

        const registerForm = document.getElementById("registerForm");

        if (registerForm) {
            registerForm.addEventListener("submit", async event => {
                event.preventDefault();

                const button = registerForm.querySelector(
                    'button[type="submit"]'
                );

                if (button) button.disabled = true;

                try {
                    const username = registerForm
                        .querySelector('[name="username"]').value.trim();

                    const email = registerForm
                        .querySelector('[name="email"]').value.trim();

                    const password = registerForm
                        .querySelector('[name="password"]').value;

                    if (password.length < 8) {
                        throw new Error(
                            "Use at least 8 characters for the password."
                        );
                    }

                    await api("/api/auth/register", {
                        method: "POST",
                        body: JSON.stringify({
                            username,
                            email,
                            password
                        })
                    });

                    showMessage(
                        registerForm,
                        "Account created. Redirecting to sign in..."
                    );

                    setTimeout(() => {
                        window.location.href = "login.html";
                    }, 700);
                } catch (error) {
                    showMessage(
                        registerForm,
                        error.message || "Registration failed.",
                        true
                    );
                } finally {
                    if (button) button.disabled = false;
                }
            });
        }

        const logoutButton = document.querySelector("[data-logout]");

        if (logoutButton) {
            logoutButton.addEventListener("click", async () => {
                try {
                    await api("/api/auth/logout", {
                        method: "POST",
                        body: "{}"
                    });
                } catch (error) {
                    console.warn(error.message);
                }

                window.location.href = "login.html";
            });
        }

        if (document.body.classList.contains("app-dashboard")) {
            api("/api/auth/me")
                .then(data => {
                    const label = document.getElementById("dashboard-user");

                    if (label && data.user) {
                        label.textContent = data.user.username;
                    }
                })
                .catch(() => {
                    window.location.replace("login.html");
                });
        }
    });
})();