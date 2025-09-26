'use client';
import { useParams, useSearchParams, useRouter } from 'next/navigation';
import React, { useEffect } from 'react';
import { OfficeHoursCard } from '@/components/custom/office-hours';
import { getCourseId, getOfficeHoursSchedule } from '@/lib/helper/database-helper';
import { Skeleton } from '@/components/ui/skeleton';
import { signOut, useSession } from 'next-auth/react';
import { getUserCoursesFromSession } from '@/lib/helper/autolab-helper';

interface UserCourse {
  auth_level: string;
  display_name: string;
  name: string;
}

interface OfficeHours {
  id: string;
  location: string;
  start: number;
  end: number;
  day: number;
  instructor: string[];
}

export default function CoursePage() {
  const [officeHours, setOfficeHours] = React.useState<OfficeHours[]>([]);
  const [loading, setLoading] = React.useState(true);

  const params = useParams();
  const searchParams = useSearchParams();
  const router = useRouter();

  const courseCode: string = params?.course as string;
  const courseName = searchParams.get('course');

  const { data: session, status } = useSession();

  // User authentication and authorization
  useEffect(() => {
    if (status === "loading") return;  // Skip while loading

    const validateUser = async () => {
      try {
        const userCourses = await getUserCoursesFromSession();
        const isAuthorized = userCourses.some(
          (course: UserCourse) =>
            course.name === courseCode && course.display_name === courseName
        );

        if (!isAuthorized) {
          // router.push('/error');
        }
      } catch (error) {
        console.error('Error occurred while fetching user courses:', error);
        // router.push('/error');
      }
    };

    if (status === 'unauthenticated') {
      signOut({
        redirect: true,
        callbackUrl: '/',
      });
    } else if (status === 'authenticated') {
      validateUser();
    }
  }, [session, status, courseCode, courseName, router]);

  // Fetch office hours data
  useEffect(() => {
    const fetchOfficeHours = async () => {
      try {
        setLoading(true);

        if (courseName && courseCode) {
          const courseId = await getCourseId(courseName, courseCode);
          if (!courseId) {
            console.error("Course ID is null");
            // router.push('/error');
            return;
          }
          
          const schedule = await getOfficeHoursSchedule(courseId);
          setOfficeHours(schedule);
        }
      } catch (error) {
        console.error('An unexpected error occurred:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchOfficeHours();
  }, [courseCode, courseName, router]);

  // Render skeletons while loading
  const renderSkeletons = () => {
    return Array.from({ length: 6 }).map((_, index) => (
      <div key={index} className="flex flex-col mb-3 space-y-2 w-full">
        <Skeleton className="h-[110px] w-full rounded-xl" />
      </div>
    ));
  };

  // Display a message if no office hours are available
  const displayMessage = () => {
    return (
      <div className="flex flex-col items-center justify-center w-full h-full py-10">
        <h1 className="text-2xl font-semibold text-muted-foreground">No office hours available</h1>
      </div>
    );
  };

  return (
    <main className="px-7 py-4">
      <h1 className="md:text-3xl text-2xl font-bold mb-4">Office Hours</h1>
      {loading
        ? renderSkeletons()
        : officeHours.length === 0
        ? displayMessage()
        : officeHours.map((OH) => (
            <OfficeHoursCard
              key={OH.id}
              id={OH.id}
              location={OH.location}
              start={OH.start}
              end={OH.end}
              day={OH.day}
              instructors={OH.instructor}
            />
          ))}
    </main>
  );
}
