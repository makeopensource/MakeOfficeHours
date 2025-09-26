'use client'

import Image from "next/image"
import React, { useEffect } from "react"
import LOGO from '../../../public/logo.png'
import ModeToggle from "./mode-toggle"
import { Button } from "../ui/button"
import Link from "next/link"
import { Avatar, AvatarFallback } from "../ui/avatar"
import { signIn, useSession } from "next-auth/react"

export default function Navbar() {
    const [auth, setAuth] = React.useState(false)
    const [loading, setLoading] = React.useState(true)
    const {data : session, status} = useSession();

    useEffect(() => {
        const fetchAuthStatus = async () => {
            try {
                setAuth(status === "authenticated");
            } finally {
                setLoading(false);
            }
        }
        fetchAuthStatus();
    }, [])

    const handleClick = async () => {
        signIn("autolab")
    };

    return (
        <nav className="flex justify-between items-center pr-5 h-20">
            <Link href="/" prefetch={false}>
                <div className="relative w-[150px] h-[200px]">
                    <Image 
                        src={LOGO} 
                        alt="logo" 
                        layout="fill"
                        style={{ objectFit: 'contain' }}
                        sizes="100px"
                    />
                </div>
            </Link>
            
            <div className="flex gap-4 items-center justify-center">
                <ModeToggle />
                {status == 'loading' ? (
                    <></>
                    // <div className="w-8 h-8 rounded-full bg-gray-300 animate-pulse"></div>
                ) : status == 'authenticated' ? (
                    <Avatar>
                        <AvatarFallback className="font-semibold">
                            MS
                        </AvatarFallback>
                    </Avatar>
                ) : (
                    <Button variant={"secondary"} className="font-semibold font-mono" onClick={handleClick}>
                        Sign Up
                    </Button>
                )}
            </div>
        </nav>
    )
}
