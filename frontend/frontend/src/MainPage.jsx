import "./MainPage.css"
import Pagination from '@mui/material/Pagination';
import Stack from '@mui/material/Stack';
import Data from "./Data";
import { useEffect } from "react";
import { useState } from "react";

export default function MainPage({ isLoggedIn }) {
    return (
        <>
            <div className="main-page">
                <div className="filtering-section">
                    {isLoggedIn ? (
                        <>
                            <button className="filtering">My Books</button>
                            <button className="filtering">Recommended Books</button>
                        </>

                    ) : null}
                </div>
                <h2 className="header">Books</h2>
                <div className='pagination'>
                    <Stack spacing={2}>
                        <Pagination
                            className='custom-pagination'
                            count={15}
                        />
                    </Stack>
                </div>
            </div>
        </>
    )
}