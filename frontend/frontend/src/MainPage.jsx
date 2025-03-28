import "./MainPage.css"
import Pagination from '@mui/material/Pagination';
import Stack from '@mui/material/Stack';
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

export default function MainPage({ isLoggedIn, searchTerm }) {
    const [books, setBooks] = useState([]);
    const [myBooks, setMyBooks] = useState([]); // books user has borrowed
    const [showMyBooks, setShowMyBooks] = useState(false);

    const user = JSON.parse(localStorage.getItem("user"));
    const userId = user?.email;

    useEffect(() => {
        fetch("http://localhost:8001/api/books")
            .then(res => res.json())
            .then(data => {
                setBooks(data);
            })
            .catch(err => {
                console.error("Error fetching books:", err);
            });
    }, []);

    useEffect(() => {
        if (isLoggedIn && userId) {
            fetch(`http://localhost:8002/mybooks/${userId}`)
                .then(res => res.json())
                .then(data => {
                    const borrowedTitles = data.map(entry => entry.book_name);
                    setMyBooks(borrowedTitles);
                })
                .catch(err => console.error("Error fetching my books:", err));
        }
    }, [isLoggedIn, userId]);

    const filteredBooks = books.filter((book) =>
        book.title.toLowerCase().includes(searchTerm.toLowerCase()) &&
        (!showMyBooks || myBooks.includes(book.title))
    );

    return (
        <div className="main-page">
            <div className="filtering-section">
                {isLoggedIn && (
                    <>
                        <button
                            className="filtering"
                            onClick={() => setShowMyBooks(false)}
                        >
                            All Books
                        </button>
                        <button
                            className="filtering"
                            onClick={() => setShowMyBooks(true)}
                        >
                            My Books
                        </button>
                        <button className="filtering">Recommended Books</button>
                    </>
                )}
            </div>

            <h2 className="header">Books</h2>

            <div className="book-list">
                {filteredBooks.map((book) => (
                    <div key={book._id} className="book-card">
                        <div className="book-info">
                            <div className="book-header">
                                <h3>{book.title}</h3>
                            </div>
                            <div className="book-image">
                                <img className="image" src={book.image} alt="" />
                            </div>
                            <p><strong>Author:</strong> {book.author}</p>
                            <p><strong>Genre:</strong> {book.genre}</p>
                            <p><strong>Type:</strong> {book.media_type}</p>
                            <p><strong>Copies:</strong> {book.available_copies}</p>
                        </div>
                        <div className="book-button">
                            <Link to={`/books/${book._id}`}><button className="button">{book.title}</button></Link>
                        </div>
                    </div>
                ))}
            </div>

            <div className='pagination'>
                <Stack spacing={2}>
                    <Pagination className='custom-pagination' count={15} />
                </Stack>
            </div>
        </div>
    );
}
