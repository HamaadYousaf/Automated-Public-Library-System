import "./MainPage.css"
import Pagination from '@mui/material/Pagination';
import Stack from '@mui/material/Stack';
import { useEffect, useState } from "react";

export default function MainPage({ isLoggedIn, searchTerm }) {
    const [books, setBooks] = useState([]);

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

    const filteredBooks = books.filter((book) =>
        book.title.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="main-page">
            <div className="filtering-section">
                {isLoggedIn && (
                    <>
                        <button className="filtering">My Books</button>
                        <button className="filtering">Recommended Books</button>
                    </>
                )}
            </div>

            <h2 className="header">Books</h2>

            <div className="book-list">
                {filteredBooks.map((book) => (
                    <div key={book._id} className="book-card">
                        <h3>{book.title}</h3>
                        <p><strong>Author:</strong> {book.author}</p>
                        <p><strong>Genre:</strong> {book.genre}</p>
                        <p><strong>Type:</strong> {book.media_type}</p>
                        <p><strong>Copies:</strong> {book.available_copies}</p>
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
