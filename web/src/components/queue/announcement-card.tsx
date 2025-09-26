import { AlertCircle } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

export default function AnnouncementCard({announcements} : {announcements : string[]}) {
    return (
        <div className="">
            <Card className="h-full flex-col items-center justify-center">
                <CardHeader className="py-5 px-5">
                    <CardTitle>
                        <h1 className="text-2xl">Announcements</h1>
                    </CardTitle>
                </CardHeader>
                <CardContent className="px-5">
                    <div className="flex flex-col space-y-3">
                        {announcements.map((announcement, index) => (
                            <div key={index} className="flex items-center gap-2">
                                <AlertCircle style={{width:"19px",height:"19px"}} color="#ef4444"/>
                                <p className="font-semibold text-muted-foreground">{announcement}</p>
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}