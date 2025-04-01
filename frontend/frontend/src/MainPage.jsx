import "./MainPage.css";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

export default function MainPage({ isLoggedIn, searchTerm }) {
    const [books, setBooks] = useState([]);
    const [myBooks, setMyBooks] = useState([]);
    const [showMyBooks, setShowMyBooks] = useState(false);
    const [showRecommended, setShowRecommended] = useState(false);
    const [recommendedBooks, setRecommendedBooks] = useState([]);
    const [selectedGenres, setSelectedGenres] = useState([]);
    const allGenres = ["Dystopian", "Poetry", "Tragedy", "Technology", "Programming", "Fantasy"];

    const user = JSON.parse(localStorage.getItem("user"));
    const userId = user?.email;

    useEffect(() => {
        fetch("http://localhost:8001/api/books")
            .then((res) => res.json())
            .then((data) => {
                setBooks(data);
            })
            .catch((err) => {
                console.error("Error fetching books:", err);
            });
    }, []);

    useEffect(() => {
        if (isLoggedIn && userId) {
            fetch(`http://localhost:8002/mybooks/${userId}`)
                .then((res) => res.json())
                .then((data) => {
                    const borrowedTitles = data.map((entry) => entry.book_name);
                    setMyBooks(borrowedTitles);
                })
                .catch((err) => console.error("Error fetching my books:", err));
        }
    }, [isLoggedIn, userId]);

    const handleGenreChange = (genre) => {
        setSelectedGenres((prev) =>
            prev.includes(genre) ? prev.filter((g) => g !== genre) : [...prev, genre]
        );
    };

    const fetchRecommendations = () => {
        fetch("http://localhost:8003/recommendations", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: userId })
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.recommended_books) {
                    setRecommendedBooks(data.recommended_books);
                } else {
                    console.warn("No recommended books returned");
                }
            })
            .catch((err) => console.error("Recommendation error:", err));
    };

    const filteredBooks = (showRecommended
        ? recommendedBooks
        : books.filter((book) =>
            book.title.toLowerCase().includes(searchTerm.toLowerCase()) &&
            (!showMyBooks || myBooks.includes(book.title))
        )
    );

    return (
        <div className="main-page">
            <div className="filtering-section">
                {isLoggedIn && (
                    <>
                        <button
                            className="filtering"
                            onClick={() => {
                                setShowMyBooks(false);
                                setShowRecommended(false);
                            }}
                        >
                            All Books
                        </button>
                        <button
                            className="filtering"
                            onClick={() => {
                                setShowMyBooks(true);
                                setShowRecommended(false);
                            }}
                        >
                            My Books
                        </button>
                        <button
                            className="filtering"
                            onClick={() => {
                                setShowRecommended(true);
                                setShowMyBooks(false);
                            }}
                        >
                            Recommended Books
                        </button>
                    </>
                )}
            </div>

            {showRecommended && (
                <div className="recommendation-section">
                    <h4>Select your preferred genres:</h4>
                    {allGenres.map((genre) => (
                        <label key={genre} style={{ marginRight: "1rem" }}>
                            <input
                                type="checkbox"
                                value={genre}
                                checked={selectedGenres.includes(genre)}
                                onChange={() => handleGenreChange(genre)}
                            />
                            {genre}
                        </label>
                    ))}
                    <button onClick={fetchRecommendations} style={{ marginLeft: "1rem" }}>
                        Get Recommendations
                    </button>
                </div>
            )}

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
                            <Link to={`/books/${book._id}`}>
                                <button className="button">{book.title}</button>
                            </Link>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
