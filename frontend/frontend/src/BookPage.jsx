import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import "./BookPage.css";

export default function BookPage() {
    const { id } = useParams(); // get the book id from the URL
    const [book, setBook] = useState(null);

    useEffect(() => {
        fetch("http://localhost:8001/api/books")
            .then(res => res.json())
            .then(data => {
                const foundBook = data.find(b => b._id === id);
                setBook(foundBook);
            })
            .catch(err => {
                console.error("Failed to load book:", err);
            });
    }, [id]);

    if (!book) return <p>Loading book details...</p>;

    return (
        <div className="book-container" >
            <h2>{book.title}</h2>
            <div className="top-section">
                <img src={book.image} alt="" />
                <div className="button-section">
                    <button>Reserve</button>
                    <button>Renew</button>
                    <button>Borrow</button>
                </div>
            </div>
            <p><strong>Author:</strong> {book.author}</p>
            <p><strong>Genre:</strong> {book.genre}</p>
            <p><strong>Published:</strong> {book.published_year}</p>
            <p><strong>Type:</strong> {book.media_type}</p>
            <p><strong>Copies Available:</strong> {book.available_copies}</p>
        </div>
    );
}
