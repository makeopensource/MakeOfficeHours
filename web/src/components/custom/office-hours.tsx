'use client'

import { CalendarPlus, Clock, Users } from "lucide-react"
import { Card, CardDescription, CardHeader, CardTitle } from "../ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar"
import { Button } from "../ui/button"
import { Badge } from "../ui/badge"
import Link from "next/link"

interface OfficeHoursCardProps {
    id: string,
    location: string,
    start: number,
    end: number,
    day: number,
    instructors: string[],
}

export const OfficeHoursCard : React.FC<OfficeHoursCardProps> = ({id, location, start, end,day, instructors}) => {
  const convertTime = (time: number): string => {
    const hours = Math.floor(time / 100); // Extract hours
    const minutes = time % 100; // Extract minutes
    const period = hours >= 12 ? 'PM' : 'AM';
    const adjustedHours = hours % 12 || 12; // Convert 0 to 12 for midnight

    return `${adjustedHours}:${minutes.toString().padStart(2, '0')} ${period}`;
};
    return (
        <div className="w-full mb-3">
        <Card key={id} className="px-4 py-3 hover:shadow-lg transition-shadow duration-300">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center space-y-4 md:space-y-0 md:space-x-4">
            <div className="flex-1 space-y-1">
              <h2 className="text-xl font-semibold">{location}</h2>
              <div className="flex items-center space-x-2 text-sm">
                <Clock className="h-4 w-4 text-muted-foreground" />
                <span className="text-muted-foreground font-semibold">{start} - {end}</span>
              </div>
              <div className="flex items-center space-x-2">
                <Users className="h-4 w-4 text-muted-foreground" />
                <div className="flex space-x-2">
                  {instructors.map((instructor, index) => (
                    <Badge className="rounded-full" key={index} variant="secondary">
                    {instructor}
                    </Badge>
                    // <Badge variant="default" key={index} className="text-xs rounded-full px-2 py-0.5">{instructor}</Badge>
                    // <div key = {index} className="border border-teal-500 bg-teal-500/20 rounded-full font-bold px-2 py-0.5 text-[10px]">
                    // {instructor}
                    // </div>
                  ))}
                </div>
              </div>
              
            </div>
            <div className="flex flex-col space-y-2 w-full md:w-auto">
              <Link className='w-full font-bold' href={{ pathname: `/queue/${id}`}}>
                <Button className="w-full font-semibold">
                  View the Queue
                </Button>
              </Link>
              <Button variant="outline" className="w-full md:w-auto font-semibold">
                <CalendarPlus className="mr-2 h-4 w-4" /> Add to Calendar
              </Button>
            </div>
          </div>
        </Card>
        </div>
    )
}