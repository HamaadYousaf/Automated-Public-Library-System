import "./Sidebar.css";
import { FaAddressBook } from "react-icons/fa";



export default function MyBooks() {
    return (
        <>
            <div className='sidebar-section'>
                <h4 className="sidebar-header">
                    <FaAddressBook /> My Books
                </h4>
            </div>
        </>
    )
}