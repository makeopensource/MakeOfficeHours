'use client'

import { BookOpen, User } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card"
import { useState, useEffect } from "react"
import QueueStatusCard from "./queue-status-card"
import { Queue } from "@/types"
import { UserCourse } from "@/types/session-types"
import { studentSessionPersistence } from "@/lib/helper/session-persistence"


interface StudentViewProps {
    queue: Queue[]
    course: UserCourse
    office_hours_id: string
    student_id: string
    handleRemoveFromQueue: (queueEntry: Queue[]) => void
}

export default function StudentView({queue, course, office_hours_id, student_id, handleRemoveFromQueue}:StudentViewProps) {
  const [loading, setLoading] = useState(false)
  const [isJoining, setIsJoining] = useState(false)
  const [hasJoinedQueue, setHasJoinedQueue] = useState(false)
  const [sessionStatus, setSessionStatus] = useState<"waiting" | "active" | "ready" | "completed">("waiting")
  const [queuePosition, setQueuePosition] = useState(0)
  const [taName, setTaName] = useState("Amit")
  const [sessionTimer, setSessionTimer] = useState("00:00")
  const [modalOpen, setModalOpen] = useState(false)

  const estimatedWaitTime = queue.length * 5

  useEffect(() => {
    const storedSession = studentSessionPersistence.loadSession();
    if(storedSession){
      setHasJoinedQueue(storedSession.hasJoinedQueue)
      setSessionStatus(storedSession.sessionStatus)
    }
  }, [])

  useEffect(() => {
    try {
      setLoading(true)
      const storedSession = studentSessionPersistence.loadSession();
      if (!storedSession || !storedSession.studentId) return;
      const studentEntry = queue.find((entry : any) => {
        return typeof entry.student === "string"
          ? entry.student === storedSession.studentId
          : entry.student.id === storedSession.studentId;
      });
      if (!studentEntry) {
        // Student is no longer in the queue — session is over or removed
        setHasJoinedQueue(false)
        setSessionStatus("waiting")
        studentSessionPersistence.clearSession()
        return
      }
      setQueuePosition(studentEntry.position)
      setHasJoinedQueue(true);
      
      // Set position
      if (studentEntry.status === "active") {
        setSessionStatus("active");
        studentSessionPersistence.saveSession({
          ...storedSession,
          sessionStatus: "active",
        });
      }else if (studentEntry.position > 1 && studentEntry.status !== "active") {
        setSessionStatus("waiting");
        studentSessionPersistence.saveSession({
          ...storedSession,
          sessionStatus: "waiting",
        });
      }else if (studentEntry.position === 1 && studentEntry.status === "waiting") {
        setSessionStatus("ready");
        studentSessionPersistence.saveSession({
          ...storedSession,
          sessionStatus: "ready",
        });
      }

      setHasJoinedQueue(true);
    } catch (error) {
      console.error("Failed to fetch queue:", error);
    } finally {
      setLoading(false);
    }
  }, [queue, office_hours_id])
  
  const validateSession = async (office_hours_id: string, student_id: string) => {
    try {
      const response = await fetch(`/api/queue/session/validate?office_hours_id=${office_hours_id}&student_id=${student_id}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });
      
      if (!response.ok) {
        console.error("Validation failed:", response.status);
        return false;
      }
      
      const data = await response.json();
      const {expired, is_valid} = data
      if(expired || !is_valid){
        alert("Please swipe your card to join the queue")
        return false
      }
      return true
    } catch (error) {
      console.error("Failed to validate session:", error);
      return false;
    }
  }
  
  const handleJoinQueue = async () => {
    try {
      setIsJoining(true);
      const valid = await validateSession(office_hours_id, student_id)
      if(!valid){
        alert("Please swipe your card to join the queue")
        return
      }
      const response = await fetch("/api/queue/join", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ office_hours_id }),
      });
  
      if (!response.ok) {
        throw new Error("Failed to join the queue");
      }
  
      const data = await response.json();
      const { position, student } = data;
  
      if (position != null && student != null) {
        setQueuePosition(position);
        setHasJoinedQueue(true);
        setSessionStatus("waiting");
  
        studentSessionPersistence.saveSession({
          hasJoinedQueue: true,
          sessionStatus: "waiting",
          office_hours_id,
          studentId: student,
        });
      } else {
        throw new Error("Position or student ID missing");
      }
    } catch (error) {
      console.error("Join error:", error);
    } finally {
      setIsJoining(false);
    }
  };
  
  
  const handleLeaveQueue = async () => {
    try {
        setIsJoining(true)
        handleRemoveFromQueue(queue.filter((q : any) => q.student === student_id))
        // const response = await fetch("/api/queue/leave",{
        //     method:"POST",
        //     headers:{
        //         "Content-Type" : "application/json"
        //     },
        //     body: JSON.stringify({office_hours_id})
        // })
        // const data = await response.json()
        // const {leftQueue} = data
        // if(!leftQueue){
        //     throw new Error("Error while removing user from the queue")
        // }

      setHasJoinedQueue(false)
      setSessionStatus("waiting")
    } catch (error) {
      console.error("Leave error:", error)
    } finally {
      setModalOpen(false)
      setIsJoining(false)
      studentSessionPersistence.clearSession()
    }
  }

  return (
        <div className="container mx-auto p-4 max-w-2xl space-y-6">
          <div className="text-center">
            <h1 className="text-3xl font-bold">Office Hours Queue</h1>
            <p className="text-muted-foreground mt-2">Track the queue status</p>
          </div>
    
          {/* Student Info Card */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <User className="h-5 w-5" />
                Student Information
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-muted-foreground">Name</p>
                  <p className="font-semibold">{"Manav Sharma"}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Course</p>
                  <p className="font-semibold flex items-center gap-1">
                    <BookOpen className="h-4 w-4" />
                    {course.display_name}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
          

          <QueueStatusCard 
            queue={queue} 
            courseName={course.name} 
            office_hours_id={office_hours_id}
            loading={loading}
            isJoining={isJoining}
            hasJoinedQueue={hasJoinedQueue}
            sessionStatus={sessionStatus}
            queuePosition={queuePosition}
            taName={taName}
            sessionTimer={sessionTimer}
            modalOpen={modalOpen}
            estimatedWaitTime={estimatedWaitTime}
            onJoinQueue={handleJoinQueue}
            onLeaveQueue={handleLeaveQueue}
            onCloseModal={() => setModalOpen(false)}
            onOpenModal={() => setModalOpen(true)}
          />
        </div>
  )
}