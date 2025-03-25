import Input from "../Components/Input"
import "./Sidebar.css";
import { TbBooks } from "react-icons/tb";

export default function BookTypes() {
    return (
        <>
            <div className='sidebar-section'>
                <h4 className="sidebar-header-book-type">
                    <TbBooks /> Book Types
                </h4>
                <div className="sidebar-list">
                    <label className="sidebar-label">
                        <input
                            type="radio"
                            value="Transit" //this will align with the value of Region (aka either downtown or a place in downtown, depending on table provided)
                            name="category"
                        />
                        Type 1
                    </label>
                    <label className="sidebar-label">
                        <input
                            type="radio"
                            value="Transit" //this will align with the value of Region (aka either downtown or a place in downtown, depending on table provided)
                            name="category"
                        />
                        Type 2
                    </label>
                    <label className="sidebar-label">
                        <input
                            type="radio"
                            value="Transit" //this will align with the value of Region (aka either downtown or a place in downtown, depending on table provided)
                            name="category"
                        />
                        Type 3
                    </label>
                    <label className="sidebar-label">
                        <input
                            type="radio"
                            value="Transit" //this will align with the value of Region (aka either downtown or a place in downtown, depending on table provided)
                            name="category"
                        />
                        Type 4
                    </label>
                    <label className="sidebar-label">
                        <input
                            type="radio"
                            value="Transit" //this will align with the value of Region (aka either downtown or a place in downtown, depending on table provided)
                            name="category"
                        />
                        Type 5
                    </label>
                </div>
            </div>
        </>
    )
} 