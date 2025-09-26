'use client'

import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "../ui/card"
import { Button } from "../ui/button"
import React from "react"
import { Skeleton } from "../ui/skeleton"
import { CheckCircle, Clock, Users } from "lucide-react"
import { AnimatedModal } from "../custom/animated-modal"
import { Separator } from "../ui/separator"
import { Badge } from "../ui/badge"
import { Queue } from "@/types"


interface QueueStatusProps {
  queue: Queue[]
  courseName: string
  office_hours_id: string
  loading: boolean
  isJoining: boolean
  hasJoinedQueue: boolean
  sessionStatus: "waiting" | "active" | "ready" | "completed"
  queuePosition: number
  taName: string
  sessionTimer: string
  modalOpen: boolean
  estimatedWaitTime: number
  onJoinQueue: () => void
  onLeaveQueue: () => void
  onCloseModal: () => void
  onOpenModal: () => void
}

export default function QueueStatus({ 
  queue, 
  courseName, 
  office_hours_id,
  loading,
  isJoining,
  hasJoinedQueue,
  sessionStatus,
  queuePosition,
  taName,
  sessionTimer,
  modalOpen,
  estimatedWaitTime,
  onJoinQueue,
  onLeaveQueue,
  onCloseModal,
  onOpenModal
}: QueueStatusProps) {

  const renderSkeleton = () => (
    <div className="flex flex-col mb-2 w-full">
      <Skeleton className="h-[225px] w-full rounded-xl" />
    </div>
  )

  return (
    <div className="w-full">
      {loading ? (
        renderSkeleton()
      ) : !hasJoinedQueue ? (
        <Card className="border-dashed border-2 border-primary/30">
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>Join Queue</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4 text-center">
            <Users className="mx-auto h-16 w-16 text-primary/60" />
            <h3 className="text-xl font-semibold mt-4">Ready to join office hours?</h3>
            <p className="text-muted-foreground">Click below to join the queue and get help from a TA.</p>

            <div className="grid grid-cols-2 gap-4 mt-4">
              <div>
                <p className="text-2xl font-bold text-primary">{queue.length}</p>
                <p className="text-sm text-muted-foreground">In Queue</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-primary">{estimatedWaitTime} min</p>
                <p className="text-sm text-muted-foreground">Est. Wait</p>
              </div>
            </div>

            <Button loading={isJoining} className="w-full mt-4" onClick={onJoinQueue}>
              Join the Queue
            </Button>
          </CardContent>
        </Card>
      ) : (
        <Card className="border-2 border-primary/20">
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>Session Status</span>
              <Badge variant={
                sessionStatus === "active" ? "default" :
                sessionStatus === "completed" ? "secondary" :
                "outline"
              }>
                {sessionStatus === "active" ? "In Progress" :
                 sessionStatus === "completed" ? "Completed" : "Waiting"}
              </Badge>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {sessionStatus === "waiting" && (
              <>
                <div className="text-center py-6">
                  <Users className="mx-auto h-16 w-16 text-primary/60" />
                  <h3 className="text-xl font-semibold mt-4">You're in the queue!</h3>
                  <p className="text-muted-foreground">Please wait for a TA to assist you</p>
                </div>

                <Separator />

                <div className="grid grid-cols-2 gap-4 text-center">
                  <div>
                    <p className="text-2xl font-bold text-primary">{queuePosition}</p>
                    <p className="text-sm text-muted-foreground">Position in Queue</p>
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-primary">{estimatedWaitTime} min</p>
                    <p className="text-sm text-muted-foreground">Estimated Wait</p>
                  </div>
                </div>

                <div className="text-center text-sm text-muted-foreground">
                  {queue.length} student{queue.length !== 1 && "s"} in queue
                </div>
              </>
            )}

            {sessionStatus === "active" && (
              <>
                <div className="text-center py-6">
                  <Clock className="mx-auto h-16 w-16 text-green-500" />
                  <h3 className="text-xl font-semibold mt-4 text-green-700">Session Active!</h3>
                  <p className="text-muted-foreground">{taName} is helping you now</p>
                </div>

                <div className="text-center">
                  <p className="text-sm text-muted-foreground mb-2">Session Duration</p>
                  <p className="text-3xl font-mono font-bold">{sessionTimer}</p>
                </div>
                <Separator />
              </>
            )}

            {sessionStatus === "ready" && (
              <>
              <div className="text-center py-6">
                <h3 className="text-xl font-semibold mt-4 text-green-700">You're up next!</h3>
                <p className="text-muted-foreground">Please wait for a TA to assist you</p>
              </div>
              <Separator />
              </>
            )}
              
                <Button loading={isJoining} variant="destructive" className="w-full mt-4" onClick={onLeaveQueue}>
                  Leave Queue
                </Button>
          </CardContent>
        </Card>
      )}

      <AnimatedModal
        header="Confirm to leave the queue"
        description="Are you sure you want to leave the queue?"
        subDescription="This action cannot be undone"
        isOpen={modalOpen}
        onClose={onCloseModal}
        onLeave={onLeaveQueue}
      />
    </div>
  )
}

