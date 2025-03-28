import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import "./BookPage.css";

export default function BookPage({ isLoggedIn }) {
    const { id } = useParams();
    const [book, setBook] = useState(null);

    const user = JSON.parse(localStorage.getItem("user"));
    const userId = user?.email || "guest@example.com";

    useEffect(() => {
        fetch("http://localhost:8001/api/books")
            .then(res => res.json())
            .then(data => {
                const actualBook = data.find(b => b._id === id);
                setBook(actualBook);
            })
            .catch(err => {
                console.error("Failed to load book:", err);
            });
    }, [id]);

    const handleReserve = () => {
        fetch(`http://localhost:8002/reserve/?user_id=${userId}&book_name=${book.title}`, {
            method: "POST"
        })
            .then(res => res.json())
            .then(data => alert(data.message))
            .catch(() => alert("Reservation failed"));
    };

    const handleBorrow = () => {
        fetch(`http://localhost:8002/borrow/?user_id=${userId}&book_name=${book.title}`, {
            method: "POST"
        })
            .then(res => res.json())
            .then(data => alert(data.message))
            .catch(() => alert("Borrow failed"));
    };

    const handleRenew = () => {
        fetch(`http://localhost:8002/renew/?user_id=${userId}&book_name=${book.title}`, {
            method: "POST"
        })
            .then(res => res.json())
            .then(data => alert(data.message))
            .catch(() => alert("Renewal failed"));
    };

    const handleReturn = () => {
        fetch(`http://localhost:8002/return/?user_id=${userId}&book_name=${book.title}`, {
            method: "POST"
        })
            .then(res => res.json())
            .then(data => alert(data.message))
            .catch(() => alert("Return failed"));
    };

    if (!book) return <p>Loading book details...</p>;

    return (
        <div className="book-container" >
            <h2>{book.title}</h2>
            <div className="top-section">
                <img src={book.image} alt="" />
                <div className="button-section">
                    {isLoggedIn && (
                        <>
                            {book.available_copies === 0 ? (
                                <button onClick={handleReserve}>Reserve</button>
                            ) : (
                                <button onClick={handleBorrow}>Borrow</button>
                            )}
                            <button onClick={handleRenew}>Renew</button>
                            <button onClick={handleReturn}>Return</button>
                        </>
                    )}
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
