import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./CommonStyles.css";

export default function Login({ setIsLoggedIn }) {
    const [loginData, setLoginData] = useState({ email: "", password: "" });
    const navigate = useNavigate();

    const handleChange = (e) => {
        setLoginData({ ...loginData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await fetch("http://localhost:8000/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(loginData),
            });

            const data = await res.json();
            if (res.ok) {
                alert("Login successful!");

                // Save user in localStorage
                localStorage.setItem("user", JSON.stringify(data.user));
                setIsLoggedIn(true); // update auth state in App
                // Redirect to main page
                navigate("/");
            } else {
                alert(`Login failed: ${data.detail}`);
            }
        } catch (err) {
            console.error("Login error:", err);
        }
    };



    return (
        <div className="card">
            <h1 className="card-header">Login</h1>
            <form onSubmit={handleSubmit}>
                <div className="card-inputs">
                    <input
                        type="email"
                        name="email"
                        placeholder="Email"
                        className="login-input"
                        required
                        onChange={handleChange}
                    />
                    <input
                        type="password"
                        name="password"
                        placeholder="Password"
                        className="login-input"
                        required
                        onChange={handleChange}
                    />
                </div>
                <div className="card-submission">
                    <button className="login-button">Login</button>
                </div>
            </form>
        </div>
    );
}
