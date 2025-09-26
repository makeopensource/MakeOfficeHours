export interface Student {
    id: string
    name: string
    email: string
    status: "waiting" | "active"
    created_at: string
    position: number
  }
  
  export interface SessionData {
    id: string
    student: Student
    startTime: Date
    isPaused: boolean
  }
  
  export interface Resolution {
    issue: string
    resolution: string
    feedback: string
  }

  export interface UserCourse {
    auth_level: string;
    display_name: string;
    name: string;
    semester: string;
  }