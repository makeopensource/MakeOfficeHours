'use server'

import { getServerSession } from "next-auth";
import { cookies } from "next/headers";
import { NextResponse } from "next/server"
import { authOptions } from "../auth/auth-option";


export async function getUserInfo({access_token}: {access_token: string}){
    const response = await fetch(process.env.AUTOLAB_USER_ENDPOINT || '', {
        method: "GET",
        headers:{
            Authorization: `Bearer ${access_token}`
        }
    })
    const userInfo = await response.json();
    if(!response.ok){
        return NextResponse.json({ error: "Error while getting user data", details: userInfo}, { status: 500 });
    }

    return userInfo;
}

export async function getUserCoursesFromAutolab({access_token}:{access_token : string}){
    try{
        const cookieStore = await cookies();
        const response = await fetch(process.env.AUTOLAB_COURSE_ENDPOINT || '',{
            method:"GET",
            headers:{
                Authorization : `Bearer ${access_token}`
            }
        })
    
        const userCourses = await response.json()
        if(!response.ok){
            return NextResponse.json({error : "Error while getting user courses", details: userCourses}, { status: 500 })
        }

        cookieStore.set("user_courses", JSON.stringify(userCourses), {
            maxAge: 60*60*2,
            httpOnly: true,
            secure: process.env.NODE_ENV === "production",
            path: "/"
        })
        return userCourses
    }catch(error){
        return NextResponse.json({error : "Error while getting user courses", details: error}, { status: 500 })
    }
}

export async function getUserCoursesFromSession(){
    try{
        const session = await getServerSession(authOptions)
        const courses = [{
            name: "cse101-f25",
            semester: "f25",
            late_slack: 0,
            display_name: "CSE 101: Test Course",
            auth_level: "instructor"
          }]
        if(session?.user?.courses){
            return [...session?.user.courses, ...courses]
        }
        else if(session?.user?.accessToken){
            const user_courses = await getUserCoursesFromAutolab({"access_token" : session?.user?.accessToken});
            return [...user_courses, ...courses];
        }
        return courses;

    }catch(error){
        return NextResponse.json({ error: "Error while getting user courses from cookies", details: error}, { status: 500 });
    }
}