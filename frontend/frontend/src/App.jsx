import { useState, useEffect } from 'react'
import { Routes, Route, BrowserRouter } from 'react-router-dom'
import './App.css'
import Navbar from './Navbar'
import Login from './Login'
import Signup from './Signup'
import Sidebar from './Sidebar/Sidebar'
import ScrollToTop from './ScrollToTop'
import MainPage from './MainPage'

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const user = localStorage.getItem("user");
    setIsLoggedIn(!!user);
  }, []);

  return (
    <>
      <BrowserRouter>
        <ScrollToTop />
        <Navbar isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} />
        {/*<div className='main-content'>
          <div className='page-content'>
            <Routes>
              <Route path='/' element={<Sidebar />} />
              <Route path='/projects/:id' element={<DetailedPages />} />
            </Routes>
          </div>
        </div>*/}
        <div className='main-content'>
          <div className='page-content'>
            <Routes>
              <Route path='/' element={<MainPage isLoggedIn={isLoggedIn} />} />
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
