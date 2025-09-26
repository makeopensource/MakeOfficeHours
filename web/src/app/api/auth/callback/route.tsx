// 'use server'

// import { NextRequest, NextResponse } from "next/server";
// import { pushUserToDataBase } from "@/lib/helper/getFromDatabase";
// import {getUserCoursesFromAutolab, getUserInfo } from "@/lib/helper/getUserInfo";
// import { cookies } from "next/headers";

// export async function GET(request: NextRequest) {
//     try{
//         const { searchParams } = new URL(request.url);
//         const code = searchParams.get("code");

//         if(!code){
//             return NextResponse.json({ message: "No code received" }, { status: 400 });
//         } 

//         const tokenResponse = await fetch("https://autolab.cse.buffalo.edu/oauth/token",{
//             method: "POST",
//             headers:{
//                 "Content-Type": "application/x-www-form-urlencoded"
//             },
//             body: new URLSearchParams({
//                 grant_type: "authorization_code",
//                 code,
//                 redirect_uri:process.env.AUTOLAB_REDIRECT_URI as string,
//                 client_id: process.env.AUTOLAB_CLIENT_ID as string,   
//                 client_secret: process.env.AUTOLAB_CLIENT_SECRET as string,
//             })
//         })

//         if(!tokenResponse.ok){
//             const error = await tokenResponse.json();
//             return NextResponse.json({ error: "Error while getting token", details:error}, { status: 500 });
//         }

//         const tokenData = await tokenResponse.json();
//         const access_token = tokenData.access_token;
//         const refresh_token = tokenData.refresh_token;
//         const expires_in = tokenData.expires_in;

//         const userData = await getUserInfo({access_token});
        
//         const userId = await pushUserToDataBase({
//             name: `${userData.first_name} ${userData.last_name}`,
//             email: userData.email,
//             access_token
//         });

//         const user_courses = await getUserCoursesFromAutolab({access_token});

//         const cookieStore = await cookies();

//         cookieStore.set("access_token", access_token, {
//             maxAge: 60*60*5,
//             httpOnly: true,
//             secure: process.env.NODE_ENV === "production",
//             path: "/"
//         });

//         cookieStore.set("refresh_token", refresh_token, {
//             maxAge: 60*60*5,
//             httpOnly: true,
//             secure: process.env.NODE_ENV === "production",
//             path: "/"
//         }); 

//         cookieStore.set("expires_at", Date.now() + expires_in, {
//             maxAge: 60*60*5,
//             httpOnly: true,
//             secure: process.env.NODE_ENV === "production",
//             path: "/"
//         })

//         cookieStore.set("user_courses", JSON.stringify(user_courses), {
//             maxAge: 60*60*5,
//             httpOnly: true,
//             secure: process.env.NODE_ENV === "production",
//             path: "/"
//         })

//         const response = NextResponse.redirect('https://localhost:3000/dashboard');
//         return response;
//     }
//     catch(error){
//         return NextResponse.json({ error: "Error occurred while getting authentication code", details : error }, { status: 500 });
//     }
// }

