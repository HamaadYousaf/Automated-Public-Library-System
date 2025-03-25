import React from 'react';
import './Navbar.css';
import { Link } from 'react-router-dom';

export default function Navbar() {

    return (
        <>
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
                        className='search-box' />
                </div>
                <div className='nav-links'>
                    <ul>
                        <li>
                            <Link to="/signup" >
                                <button className='nav-button'>Sign Up</button>
                            </Link>
                        </li>
                        <li>
                            <Link to="/login" >
                                <button className='nav-button'>Login</button>
                            </Link>
                        </li>
                    </ul>
                </div>
            </nav>
        </>
    )
}
