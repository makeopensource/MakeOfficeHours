"use client"
import { useState, useEffect } from "react"
import type { SessionData } from "@/types/session-types"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Clock, Pause, Play, StopCircle, User, CircleAlert } from "lucide-react"

interface ActiveSessionProps {
  session: SessionData
  onEndSession: () => void
  onTogglePause: () => void
  setTime: (time: number) => void
  handleDeleteSession: () => void
}

export function ActiveSession({ session, onEndSession, onTogglePause, setTime, handleDeleteSession }: ActiveSessionProps) {
  const [elapsedTime, setElapsedTime] = useState(0)
  const [formattedTime, setFormattedTime] = useState("00:00")
  const [pausedTime, setPausedTime] = useState(0) // Track total paused time
  const [pauseStartTime, setPauseStartTime] = useState<number | null>(null)

  // Calculate and update elapsed time
  useEffect(() => {
    if (!session) return

    // Handle pause state changes
    if (session.isPaused) {
      if (pauseStartTime === null) {
        setPauseStartTime(Date.now())
      }
      return
    } else {
      // If resuming from pause, add the paused duration to total paused time
      if (pauseStartTime !== null) {
        setPausedTime(prev => prev + (Date.now() - pauseStartTime))
        setPauseStartTime(null)
      }
    }

    const startTime = session.startTime.getTime()
    const interval = setInterval(() => {
      const now = Date.now()
      const totalElapsed = now - startTime
      const activeElapsed = Math.floor((totalElapsed - pausedTime) / 1000)
      
      setElapsedTime(activeElapsed)
      
      // Format time as MM:SS
      const minutes = Math.floor(activeElapsed / 60)
      const seconds = activeElapsed % 60
      setFormattedTime(`${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`)
    }, 1000)

    return () => clearInterval(interval)
  }, [session, pausedTime, pauseStartTime])

  // Reset paused time when session changes
  useEffect(() => {
    setPausedTime(0)
    setPauseStartTime(null)
    setElapsedTime(0)
  }, [session?.startTime])

  const handleEndSession = () => {
    setTime(elapsedTime)
    onEndSession()
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold">Active Session</h2>
        <div className="flex items-center gap-2">
          <Clock className="h-5 w-5 text-muted-foreground" />
          <span className="text-xl font-mono">{formattedTime}</span>
        </div>
      </div>

      <Card className="border-2 border-primary/20">
        <CardContent className="pt-6">
          <div className="grid gap-6 md:grid-cols-2">
            <div className="space-y-4">
              <div className="flex items-center gap-2">
                <User className="h-5 w-5 text-muted-foreground" />
                <h3 className="text-lg font-medium">Student</h3>
              </div>
              <div className="pl-7">
                <p className="text-lg font-semibold">{session.student.name}</p>
              </div>
            </div>
            <div className="space-y-4"> 
              <div className="flex items-center gap-2"> 
                <h3 className="text-lg font-medium">Other Information</h3>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="flex flex-col sm:flex-row gap-4 justify-center">
        <Button onClick={onTogglePause} variant="outline" className="flex-1">
          {session.isPaused ? (
            <>
              <Play className="mr-2 h-4 w-4" /> Resume Session
            </>
          ) : (
            <>
              <Pause className="mr-2 h-4 w-4" /> Pause Session
            </>
          )}
        </Button>
        <Button onClick={handleEndSession} variant="default" className="flex-1">
          <StopCircle className="mr-2 h-4 w-4" /> End Session
        </Button>
        {handleDeleteSession &&<Button onClick={handleDeleteSession} variant="destructive" className="flex-1">
          <CircleAlert className="mr-2 h-4 w-4" /> Delete Session
        </Button>}
      </div>
    </div>
  )
}