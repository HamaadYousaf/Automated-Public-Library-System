import React from 'react';
import './Navbar.css';
import { Link, useNavigate } from 'react-router-dom';

export default function Navbar({ isLoggedIn, setIsLoggedIn, searchTerm, setSearchTerm }) {
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem("user");
        setIsLoggedIn(false);
        navigate("/login");
    };

    return (
        <nav className='navbar'>
            <div className="nav-logo">
                <Link to="/">
                    <div className='logo'><span>Library</span>Hub</div>
                </Link>
            </div>
            <div className='nav-input'>
                <input
                    type="text"
                    placeholder='Search for books...'
                    className='search-box'
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
            </div>
            <div className='nav-links'>
                <ul>
                    {!isLoggedIn ? (
                        <>
                            <li>
                                <Link to="/signup">
                                    <button className='nav-button'>Sign Up</button>
                                </Link>
                            </li>
                            <li>
                                <Link to="/login">
                                    <button className='nav-button'>Login</button>
                                </Link>
                            </li>
                        </>
                    ) : (
                        <li>
                            <button className='nav-button' onClick={handleLogout}>
                                Logout
                            </button>
                        </li>
                    )}
                </ul>
            </div>
        </nav>
    );
}
