import MainPage from "../MainPage";
import MyBooks from "./MyBooks";
import RecommendedBooks from "./RecommendedBooks";
import BookTypes from "./BookTypes";

export default function Sidebar() {

    return (
        <>
            {/*<div className="sidebar">
                <MyBooks />
                <RecommendedBooks />
                <BookTypes />
            </div>*/}
            <MainPage />
        </>
    );
}
