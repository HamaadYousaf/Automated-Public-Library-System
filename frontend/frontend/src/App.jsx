import { useState, useEffect } from 'react'
import { Routes, Route, BrowserRouter } from 'react-router-dom'
import './App.css'
import Navbar from './Navbar'
import Login from './Login'
import Signup from './Signup'
import ScrollToTop from './ScrollToTop'
import MainPage from './MainPage'
import BookPage from './BookPage'

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    const user = localStorage.getItem("user");
    setIsLoggedIn(!!user);
  }, []);

  return (
    <>
      <BrowserRouter>
        <ScrollToTop />
        <Navbar isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} searchTerm={searchTerm}
          setSearchTerm={setSearchTerm} />
        <div className='main-content'>
          <div className='page-content'>
            <Routes>
              <Route path='/' element={<MainPage isLoggedIn={isLoggedIn} searchTerm={searchTerm} />} />
              <Route path='/books/:id' element={<BookPage isLoggedIn={isLoggedIn} />} />
              <Route path='/signup' element={<Signup />} />
              <Route path='/login' element={<Login setIsLoggedIn={setIsLoggedIn} />} />
            </Routes>
          </div>
        </div>
      </BrowserRouter>
    </>
  )
}

export default App
