"use client"

import type React from "react"

import { useState } from "react"
import type { Student } from "@/types/session-types"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,      
} from "@/components/ui/dialog"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { useSession } from "next-auth/react"

interface ResolutionFormProps {
  student: Student
  onSubmit: (resolution: { issue: string; resolution: string; feedback: string; taEmail: string; studentEmail: string }) => void
  onCancel: () => void
}

export function ResolutionForm({ student, onSubmit, onCancel }: ResolutionFormProps) {
  const [issue, setIssue] = useState("")
  const [resolution, setResolution] = useState("")
  const [feedback, setFeedback] = useState("")

  const { data: session, status } = useSession();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!session?.user?.email) return
    onSubmit({ issue, resolution, feedback, taEmail: session.user.email, studentEmail: student.email })
  }

  return (
    <Dialog open={true} onOpenChange={() => onCancel()}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>Session Resolution</DialogTitle>
          <DialogDescription>
            Please provide details about the session with {student.name}.
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6 py-4">
          <div className="space-y-2">
            <Label htmlFor="issue" className="text-right">
              Issue Description <span className="text-destructive">*</span>
            </Label>
            <Textarea
              id="issue"
              placeholder="Describe the student's issue or query"
              value={issue}
              onChange={(e) => setIssue(e.target.value)}
              required
              className="min-h-[100px]"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="resolution" className="text-right">
              Resolution <span className="text-destructive">*</span>
            </Label>
            <Textarea
              id="resolution"
              placeholder="Describe the solution provided or next steps"
              value={resolution}
              onChange={(e) => setResolution(e.target.value)}
              required
              className="min-h-[100px]"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="feedback" className="text-right">
              TA Feedback (Optional)
            </Label>
            <Textarea
              id="feedback"
              placeholder="Any additional feedback about the session"
              value={feedback}
              onChange={(e) => setFeedback(e.target.value)}
              className="min-h-[80px]"
            />
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={onCancel}>
              Cancel
            </Button>
            <Button type="submit">Submit Resolution</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
