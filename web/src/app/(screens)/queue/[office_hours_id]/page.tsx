'use client'

import { Skeleton } from "@/components/ui/skeleton";
import { getCourseName, getOfficeHoursEntry } from "@/lib/helper/database-helper";
import { getUserCoursesFromSession } from "@/lib/helper/autolab-helper";
import { getQueue, removeFromQueue } from "@/lib/helper/queue-helper";
import { signOut, useSession } from "next-auth/react";
import { useParams } from "next/navigation";
import React, { useEffect, useState } from "react";
import type { Queue } from "@/types";
import InstructorView from "@/components/queue/instructor-view";
import StudentView from "@/components/queue/student-view";
import { UserCourse } from "@/types/session-types";
import { Button } from "@/components/ui/button";
import { getClientSupabaseClient } from "@/lib/supabase/supabase-client";
import { SupabaseClient } from "@supabase/supabase-js";



export default function QueuePage() {
  const [authLevel, setAuthLevel] = React.useState<"student" | "instructor" | null>(null);
  const [loading, setLoading] = React.useState(true);
  const [course, setCourse] = React.useState<UserCourse>();
  const [queue, setQueue] = React.useState<Queue[]>([]);
  const [error, setError] = React.useState<string | null>(null);
  const { data: session, status } = useSession();
  const params = useParams();
  const office_hours_id: string = params?.office_hours_id as string;
  // Validate queue and fetch course and user details
  React.useEffect(() => {
    const validateQueue = async () => {
      try {
        setLoading(true);
        setError(null);

        const officeHourEntry = await getOfficeHoursEntry(office_hours_id);
        if (!officeHourEntry) {
          setError("Invalid office hours queue.");
          return;
        }

        const current_course = await getCourseName(officeHourEntry.class);
        const user_courses = await getUserCoursesFromSession();
        const user_course = Array.isArray(user_courses) ? user_courses.find(
          (course: any) =>
            course.display_name === current_course.name &&
            course.name === current_course.code
        ) : null;

        if (!user_course) {
          setError("User is not authorized to view this queue.");
          return;
        }

        setCourse(user_course);
        setAuthLevel(user_course.auth_level);
      } catch (error) {
        console.error("Error while validating queue:", error);
        setError("An unexpected error occurred. Please try again.");
      } finally {
        setLoading(false); // Ensure loading state is set to false once validation is complete
      }
    };

    if (status === "unauthenticated") {
      signOut({
        redirect: true,
        callbackUrl: "/",
      });
    } else {
      validateQueue();
    }
  }, [status, session, office_hours_id]);

  // Fetch queue info
  React.useEffect(() => {
    const getQueueInfo = async () => {
      try {
        setLoading(true);
        const fetchedQueue = await getQueue(office_hours_id);

        if (!fetchedQueue) {
          console.error("Error while fetching queue info");
          return;
        }
        if (Array.isArray(fetchedQueue)) {
          setQueue(fetchedQueue);
        } else {
          console.error("Queue is not an array");
        }
      } catch (error) {
        console.error("Error while fetching queue info:", error);
      } finally {
        setLoading(false); // Ensure loading state is set to false once fetching is complete
      }
    };

    if (status !== "unauthenticated") {
      getQueueInfo();
    }
  }, [status, session, office_hours_id]);

  const enrichQueueEntry = async (entry: any): Promise<Queue> => {
    try {
      const response = await fetch(`/api/users?id=${entry.student}`)
      if(!response.ok){
        console.error("Error while fetching user", response.statusText)
        return entry
      }
      const data = await response.json()
      return {
        ...entry,
        name: data.name,
        email: data.email,
      };
    } catch (err) {
      console.error("Failed to enrich queue entry:", err);
      return entry;
    }
  };
  

  useEffect(() => {
    let channel: ReturnType<SupabaseClient['channel']> | null = null;
    const setupRealtime = async () => {
      const supabase = await getClientSupabaseClient()
      channel = supabase.channel("realtime-queue").on(
        "postgres_changes",
        {
          event: "*",
          schema: "public",
          table: "queue",
        },
        async (payload) => {
          if (payload.eventType === "INSERT" && payload.new) {
            const newQueueEntry = payload.new as Queue;
            if (newQueueEntry.office_hours !== office_hours_id) return;
          
            setQueue((prev) => {
              const alreadyExists = prev.some(q => q.id === newQueueEntry.id);
              if (alreadyExists) return prev;
          
              if (!newQueueEntry.name || !newQueueEntry.email) {
                enrichQueueEntry(newQueueEntry).then(enriched => {
                  setQueue(current =>
                    current.some(q => q.id === enriched.id) ? current : [...current, enriched]
                  );
                });
                return prev;
              } else {
                return [...prev, newQueueEntry];
              }
            });
          }
          
      
          if (payload.eventType === "UPDATE" && payload.new) {
            const updatedEntry = payload.new as Queue;
            if (updatedEntry.office_hours !== office_hours_id) return;
      
            const enriched = await enrichQueueEntry(updatedEntry);
            setQueue((prev) =>
              prev.map((q) => (q.id === enriched.id ? enriched : q))
            );
          }
      
          if (payload.eventType === "DELETE" && payload.old) {
            const deletedEntry = payload.old as Queue;
            setQueue((prev) => prev.filter(q => q.id !== deletedEntry.id));
          }
        }
      ).subscribe()
      
    }
  
    setupRealtime()
  
    return () => {
      if (channel) {
        channel.unsubscribe()
      }
    }
  }, [office_hours_id])

  // Render skeletons while loading
  const renderSkeletons = () => (
    <div>
      {Array.from({ length: 6 }).map((_, index) => (
        <div key={index} className="flex flex-col mb-3 w-full lg:w-[350px]">
          <Skeleton className="h-[200px] w-full rounded-xl lg:w-[350px]" />
        </div>
      ))}
    </div>
  );

  const handleRemoveFromQueue = async (queueEntry: Queue[]) => {
    const updatedQueue = await removeFromQueue(queueEntry);
    console.log(queueEntry)
    console.log(updatedQueue)
    if (queueEntry) {
      setQueue((prevQueue) => {
        const updatedQueue = prevQueue.filter((entry) => !queueEntry.includes(entry));
        return updatedQueue.map((entry, index) => ({
          ...entry,
          position: index + 1,
        }));
      });
    } else {
      console.error("Error while removing from queue");
    }
  };

  const renderStudentView = () => (
    <div className="flex-col space-y-4">
      <StudentView 
        queue={queue} 
        course={course!}
        office_hours_id={office_hours_id}
        student_id={session?.user?.id!}
        handleRemoveFromQueue={handleRemoveFromQueue}
      />
    </div>
  );

  const renderInstructorView = () => (
    <div className="">
      <InstructorView 
      queueState={queue} 
      handleRemoveFromQueue={handleRemoveFromQueue}
      office_hours_id={office_hours_id}
      />
    </div>
  );

  // // If still loading or auth level is not set
  // if (authLevel === null) {
  //   return <main className="px-7 py-4">{renderSkeletons()}</main>;
  // }

  // If there is an error, display it
  if (error) {
    return <main className="px-7 py-4">{error}</main>;
  }

  // Handle rendering based on auth level
  return (
    <main className="px-7 py-4">
      <Button onClick={() => setAuthLevel(authLevel === "student" ? "instructor" : "student")}>
        change view
      </Button>
      {authLevel === "student" ? renderStudentView() : renderInstructorView()}
    </main>
  );
}
