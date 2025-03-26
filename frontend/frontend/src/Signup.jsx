import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./CommonStyles.css";

export default function Signup() {
    const [formData, setFormData] = useState({
        email: "",
        name: "",
        password: "",
        preferences: []
    });

    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await fetch("http://localhost:8000/users", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData),
            });

            const data = await res.json();
            if (res.ok) {
                navigate("/login");
            } else {
                alert(`Signup failed: ${data.detail}`);
            }
        } catch (err) {
            console.error("Signup error:", err);
        }
    };

    return (
        <div className="card">
            <h1 className="card-header">Sign Up</h1>
            <form onSubmit={handleSubmit}>
                <div className="card-inputs">
                    <input
                        type="email"
                        name="email"
                        placeholder="E-mail"
                        className="card-input"
                        required
                        onChange={handleChange}
                    />
                    <input
                        type="text"
                        name="name"
                        placeholder="Name"
                        className="card-input"
                        required
                        onChange={handleChange}
                    />
                    <input
                        type="password"
                        name="password"
                        placeholder="Password"
                        className="card-input"
                        required
                        onChange={handleChange}
                    />
                </div>
                <div className="card-submission">
                    <button className="signup-button">Sign Up</button>
                </div>
            </form>
        </div>
    );
}
