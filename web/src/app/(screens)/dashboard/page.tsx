'use client'

import { CourseCard } from '@/components/custom/course-card';
import React, {useEffect} from 'react';
import { Skeleton } from '@/components/ui/skeleton';
import {getUserCoursesFromSession } from '@/lib/helper/autolab-helper';
import { signOut, useSession } from 'next-auth/react';
import { UserCourse } from '@/types/session-types';

export default function Dashboard() {
  const [userCourses, setUserCourses] = React.useState<UserCourse[]>([]);
  const [loading, setLoading] = React.useState(true);

  const { data: session, status } = useSession();

  useEffect(() => {
    const fetchUserCourses = async () => {
      try {
        setLoading(true);
        const user_courses = await getUserCoursesFromSession();
        if(Array.isArray(user_courses)){
          setUserCourses(user_courses);
          return;
        }else{
          setUserCourses([]);
        }
      } catch (error) {
        console.error("An error occurred while fetching user courses:", error);
      } finally {
        setLoading(false);
      }
    };
  
    if (status === 'unauthenticated') {
      signOut({
        redirect: true,
        callbackUrl: '/',
      });
    } else if (status === 'authenticated') {
      fetchUserCourses();
    }
  }, [session, status]);

  const renderSkeletons = () => {
    return Array.from({ length: 6 }).map((i, index) => (
      <div key={index} className="flex flex-col space-y-2 w-full lg:w-[350px]">
        <Skeleton className="h-[150px] w-full rounded-xl lg:w-[350px]" />
      </div>
    ));
  };

  return (
    <main className='px-7 py-4'>
        <h1 className='md:text-3xl text-2xl font-bold mb-4'>Dashboard</h1>
        <div className='flex flex-wrap gap-4'>
        {loading?
        renderSkeletons()
        : userCourses.length > 0 ? 
        userCourses.map((course) => {
                return(
                    <CourseCard 
                    key={course.name}
                    courseName={course.display_name}
                    courseCodeName={course.name}
                    description={"Very good course"}
                    instructor={course.auth_level == "instructor" ? true : false}
                    officeHours={5}
                    />
                )
            })
          :
          <h1 className='mx-auto mt-[10rem] text-3xl font-semibold'>You don't have any current courses!</h1>
          }
        </div>
    </main>
  );
}

