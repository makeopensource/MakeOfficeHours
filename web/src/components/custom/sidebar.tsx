'use client'

import { 
  ListEnd, 
  Home, 
  MessageSquareQuote, 
  UserRoundPen, 
  BookOpen, 
  ChevronsUpDown,
  LogOut, 
  CircleAlert, 
  MoonIcon, 
  SunIcon } from "lucide-react"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"
import React, { useEffect } from "react"
import { Skeleton } from "../ui/skeleton"
import { getUserCoursesFromAutolab, getUserCoursesFromSession } from "@/lib/helper/autolab-helper"
import { DropdownMenu, DropdownMenuContent, DropdownMenuGroup, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "../ui/dropdown-menu"
import { useTheme } from "next-themes"
import { signOut, useSession } from "next-auth/react"
import { useRouter } from "next/navigation"

interface UserCourse{
  auth_level:string,
  display_name:string,
  name:string,
}

const menu_items = [
  {
    title: "Dashboard",
    url: "/dashboard",
    icon: Home,
  },
  {
    title: "Queue",
    url: "/dashboard",
    icon: ListEnd,
  },
  {
    title: "Feedback",
    url: "/dashboard",
    icon: MessageSquareQuote,
  },
  {
    title: "Profile",
    url: "/dashboard",
    icon: UserRoundPen,
  },
]

export function AppSidebar() {
  const [courses, setCourses] = React.useState<UserCourse[]>([]);
  const [loading, setLoading] = React.useState(true);
  const { theme, setTheme } = useTheme();

  const { data: session, status } = useSession();

  useEffect(() => {
    const fetchUserCourses = async () => {
      try {
        setLoading(true);
        const user_courses = await getUserCoursesFromSession();
        if(user_courses){
          setCourses(user_courses);
          return;
        }else{
          setCourses([]);
        }
      } catch (error) {
        console.error("An error occurred while fetching user courses:", error);
      } finally {
        setLoading(false);
      }
    };
  
    if (status === "authenticated") {
      fetchUserCourses();
    }
  }, [session, status]);

  const handleLogOut = async () => {
    try {
      await signOut({
        redirect: true,
        callbackUrl: '/',
      });
    } catch (error) {
      console.error("Error during logout:", error);
    }
  };
  
  const renderCourseSkeleton = () => {
      return Array.from({ length: 6 }).map((i, index) => (
        <Skeleton key={index} className="h-7 rounded-sm" />
      ));
    };

  return (
    <Sidebar suppressHydrationWarning={true}>
      <SidebarHeader>
        <h1 className="text-center py-2 font-bold">Next Up</h1>
      {/* <Image
            src={LOGO}
            alt="NextUp"
            width={100}
            height={100}
            layout="intrinsic" // Ensure intrinsic size
            className="object-contain" // Ensures the image fills only its intrinsic bounds
          /> */}
      </SidebarHeader>
      <SidebarContent className="px-1">
        <SidebarGroup >
          <SidebarGroupLabel className="text-sm font-semibold">Menu</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {menu_items.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild>
                    <a href={item.url}>
                      <item.icon />
                      <span className="font-semibold">{item.title}</span>
                    </a>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
        <SidebarGroup>
        {courses.length > 0 ? <SidebarGroupLabel className="text-sm font-semibold">Courses</SidebarGroupLabel> : null}
          <SidebarGroupContent>
            <SidebarMenu >
              {loading 
              ? <div suppressHydrationWarning={true} className="flex flex-col space-y-2">
                {renderCourseSkeleton()}
                </div>
              : Array.isArray(courses) && courses.length > 0
              ? courses.map((item) => (
                <SidebarMenuItem key={item.name}>
                  <SidebarMenuButton asChild>
                    <a href={"/"}>
                      <BookOpen />
                      <span className="font-semibold">{item.display_name}</span>
                    </a>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))
            : null}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
      <DropdownMenu modal={false}>
          <DropdownMenuTrigger asChild>
            <SidebarMenuButton className="h-10">
              <div suppressHydrationWarning={true} className="dark:bg-slate-800 bg-gray-300 p-1.5 rounded-full">
                <span className="font-semibold">MS</span>
              </div>
              <h1 className="font-semibold">Manav Sharma</h1>
                <ChevronsUpDown style={{ width: '20px', height: '20px' }} className="ml-auto" />
            </SidebarMenuButton>
          </DropdownMenuTrigger>
          <DropdownMenuContent className="w-[--radix-popper-anchor-width]">
          <DropdownMenuGroup>
            {/* <DropdownMenuLabel>
              <div className="flex items-center gap-2">
                <div className="bg-slate-800 p-1.5 rounded-full">
                  <span className="font-semibold">MS</span>
                </div>
                <div className="grid flex-1 text-left text-sm leading-tight">
                  <h1 className="text-[11px]">Manav Sharma</h1>
                  <p className="text-[10px]">manavsha@buffalo.edu</p>
                </div>
              </div>
            </DropdownMenuLabel>
            <DropdownMenuSeparator/> */}
                <DropdownMenuItem>
                    <MessageSquareQuote/>
                    Feedback
                </DropdownMenuItem>
                <DropdownMenuItem>
                    <CircleAlert size={16} />
                    Report Issue
                </DropdownMenuItem>
            </DropdownMenuGroup>
            <DropdownMenuGroup>
              <DropdownMenuItem onClick={() => setTheme(theme === "dark" ? "light" : "dark")}>
                {theme === "dark" ? <SunIcon size={16} /> : <MoonIcon size={16} />}
                Change Theme
              </DropdownMenuItem>
            </DropdownMenuGroup>
            <DropdownMenuSeparator/>
            <DropdownMenuGroup>
                <DropdownMenuItem onClick={handleLogOut}>
                    <LogOut size={16} />
                    Log Out
                </DropdownMenuItem>
            </DropdownMenuGroup>
          </DropdownMenuContent>
        </DropdownMenu>
      </SidebarFooter>
    </Sidebar>
  )
}
