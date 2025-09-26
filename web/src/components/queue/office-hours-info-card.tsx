import { Book, BookMarked, Clock, MapPin, UserRound } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Badge } from "../ui/badge";

export default function OfficeHoursInfoCard(){
    return(
        <div>
            <Card>
                <CardHeader className="py-5 px-5">
                    <CardTitle>
                        <h1 className="text-2xl">Office Hours Information</h1>
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="grid grid-cols-2 gap-2">
                        <div className="flex-col gap-1">
                            <div className="flex items-center gap-0.5">
                                <MapPin style={{width:"18px",height:"18px"}}/>
                                <h1 className="text-lg font-bold">Location</h1>
                            </div>
                            <p className="text-sm text-muted-foreground font-semibold">Davis Carl's Corner</p>
                        </div>
                        <div className="flex-col gap-1">
                            <div className="flex items-center gap-1">
                                <BookMarked style={{width:"17px",height:"17px"}}/>
                                <h1 className="text-lg font-bold">Course</h1>
                            </div>
                            <p className="text-sm text-muted-foreground font-semibold">CSE 220: Systems Programming</p>
                        </div>
                        <div className="flex-col gap-1">
                            <div className="flex items-center gap-0.5">
                                <UserRound style={{width:"17px",height:"17px"}}/>
                                <h1 className="text-lg font-bold">Instructors</h1>
                            </div>
                            <div className="flex items-center gap-2">
                                <Badge className="px-1">John Doe</Badge>
                            </div>
                        </div>
                        <div className="flex-col gap-1">
                            <div className="flex items-center gap-1">
                                <Clock style={{width:"17px",height:"17px"}}/>
                                <h1 className="text-lg font-bold">Time</h1>
                            </div>
                            <p className="text-sm text-muted-foreground font-semibold">8:00 Am - 10:00 Am</p>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}