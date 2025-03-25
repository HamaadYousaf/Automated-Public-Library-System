import "./Sidebar.css";
import { FaBook } from "react-icons/fa";


export default function RecommendedBooks() {
    return (
        <>
            <div className='sidebar-section'>
                <h4 className="sidebar-header">
                    <FaBook /> Recommended Books
                </h4>
            </div>
        </>
    )
}