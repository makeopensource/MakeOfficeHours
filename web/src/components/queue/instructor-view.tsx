"use client"
import { CardInputModal } from "../custom/card-input-modal";
import type { Queue } from "@/types/queue-types";
import { Button } from "../ui/button";
import { useState, useEffect } from "react"
import { QueueStatusTable } from "./queue-status-table"
import { ActiveSession } from "@/components/queue/active-session"
import { ResolutionForm } from "@/components/queue/resolution-form"
import type { Student, SessionData } from "@/types/session-types"
import { Card, CardContent } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { sessionPersistence } from "@/lib/helper/session-persistence";

interface InstructorViewProps {
    queueState: Queue[];
    handleRemoveFromQueue: (queueEntry: Queue[]) => void
    office_hours_id: string
}

export default function InstructorView({queueState, handleRemoveFromQueue, office_hours_id}: InstructorViewProps) {
  const [activeSession, setActiveSession] = useState<SessionData | null>(null)
  const [showResolutionForm, setShowResolutionForm] = useState(false)
  const [activeTab, setActiveTab] = useState<string>("queue")
  const [time, setTimeTaken] = useState<number>(0)
  const [modalOpen, setModalOpen] = useState(false);
  const [loading, setLoading] = useState(false)

  const handleModalOpen = () => {
    setModalOpen(true);
  };

  const handleModalClose = () => {
    setModalOpen(false);
  };

  const handleFormSubmit = (formData: FormData) => {
    console.log(formData)
  }

  useEffect(() => {
    const storedSession = sessionPersistence.loadSession();
    if (storedSession) {
      const now = new Date()
      const sessionAge = now.getTime() - new Date(storedSession.startTime).getTime()
      const maxSessionAge = 1000 * 60 * 60 * 4
      if (sessionAge < maxSessionAge) {
        setActiveSession(storedSession)
        setActiveTab("active-session")
      } else {
        sessionPersistence.clearSession()
      }
    }
  }, []);

  useEffect(() => {
    const handleBeforeUnload = (e: BeforeUnloadEvent) => {
      if (activeSession && !showResolutionForm) {
        e.preventDefault()
        e.returnValue = "You have an active session. Are you sure you want to leave?"
        return "You have an active session. Are you sure you want to leave?"
      }
    }

    if (activeSession) {
      window.addEventListener("beforeunload", handleBeforeUnload)
    }

    return () => {
      window.removeEventListener("beforeunload", handleBeforeUnload)
    }
  }, [activeSession, showResolutionForm])


  // Start a session with a student
  const startSession = async (queue: Queue) => {
    // check if the student is already being helped by another instructor
    try {
      setLoading(true)
      const isActive = queueState.some(q => q.id === queue.id && q.status === "active")
      if(isActive){
        alert("Student is already being helped by another instructor")
        return
      }
      const student = {
        id: queue.id,
        name: queue.name,
        email: queue.email,
        status: "active" as const,
        created_at: new Date().toISOString(),
        position: queue.position,
      }
      const newSession = {
        id: `session-${Date.now()}`,
        student,
        startTime: new Date(),
        isPaused: false,
      }
      const response = await fetch(`/api/queue/session/update`, {
        method: "POST",
        body: JSON.stringify({id: queue.id, status: "active"}),
      })  
      if (!response.ok) {
        throw new Error("Failed to start session")
      }
      setActiveSession(newSession)
      if (sessionPersistence.hasStoredSession()){
          sessionPersistence.clearSession()
      }
      sessionPersistence.saveSession(newSession)
      setActiveTab("active-session")
      
    } catch (error) {
      console.error("Error while starting session:", error)
    }finally{
      setLoading(false)
    }

  }

  // End the current session
  const endSession = async () => {
    try {
      setShowResolutionForm(true)
    } catch (error) {
      console.error("Error while ending session:", error)
    }
  }

  // Pause or resume the current session
  const togglePauseSession = () => {
    if (activeSession) {
        const updatedSession = {
            ...activeSession,
            isPaused: !activeSession.isPaused,
          }
    
        setActiveSession(updatedSession)
    
        // Save updated session to localStorage
        sessionPersistence.saveSession(updatedSession)
    }
  }

  const submitResolution = (resolution: { issue: string; resolution: string; feedback: string; taEmail: string; studentEmail: string; time?: number }) => {
    resolution.time = time
    console.log(resolution)
    sessionPersistence.clearSession()
    setActiveSession(null)
    setShowResolutionForm(false)
    setActiveTab("queue")
    handleRemoveFromQueue(queueState.filter(q => q.email === resolution.studentEmail))
  }

  const handleDeleteSession = async () => {
    try {
      const response = await fetch(`/api/queue/session/update`, {
        method: "POST",
        body: JSON.stringify({id: activeSession?.student.id, status: "waiting"}),
      })
      if (!response.ok) {
        throw new Error("Failed to end session")
      }
      if (activeSession) {
        sessionPersistence.clearSession()
        setActiveSession(null)
        setShowResolutionForm(false)
        setActiveTab("queue")
      }
    } catch (error) {
      console.error("Error while deleting session:", error)
    }
  }

  return (
    <div className="container mx-auto p-4 max-w-7xl">
      <h1 className="text-3xl font-bold mb-6">Office Hours Queue</h1>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-2 mb-6">
          <TabsTrigger value="queue">Student Queue</TabsTrigger>
          <TabsTrigger value="active-session" disabled={!activeSession}>
            Active Session
          </TabsTrigger>
        </TabsList>

        <TabsContent value="queue" className="space-y-4">
          <Card>
            <CardContent className="pt-6">
              <QueueStatusTable queue={queueState} handleRemoveFromQueue={handleRemoveFromQueue} handleStartSession={startSession} loading={loading} />
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="active-session" className="space-y-4">
          {activeSession && (
            <Card>
              <CardContent className="pt-6">
                <ActiveSession 
                    session={activeSession} 
                    onEndSession={endSession} 
                    onTogglePause={togglePauseSession} 
                    setTime={setTimeTaken} 
                    handleDeleteSession={handleDeleteSession} />
              </CardContent>
            </Card>
          )}
        </TabsContent>
      </Tabs>

      {showResolutionForm && activeSession && (
        <ResolutionForm
          student={activeSession.student}
          onSubmit={submitResolution}
          onCancel={() => setShowResolutionForm(false)}
        />
      )}

        <div className="flex justify-center mt-4">
            <Button
              variant={"primary"}
              size={"default"}
              onClick={handleModalOpen}
              className="font-semibold"
            >
              Add a student
            </Button>
        </div>

            <CardInputModal
                header="Queue Form"
                isOpen={modalOpen}
                onClose={handleModalClose}
                onSubmit={handleFormSubmit}
            />
    </div>
  )
}




