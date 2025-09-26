'use client'

import { ShinyText } from "@/components/custom/shiny-text";
import { Button } from "../../components/ui/button";
import { useRouter } from "next/navigation";
import { signIn } from "next-auth/react";

export default function Home() {
  const router = useRouter();

  const handleClick = async () => {
    signIn("autolab")
  };
  return (
    <main className="flex flex-col items-center justify-center pt-[9rem]">
      <div className="text-center flex flex-col items-center gap-3 p-5">
        <ShinyText className="shiny-text">JOIN THE QUEUE</ShinyText>
        <p style={{lineHeight:"2rem"}} className="max-w-[800px] font-medium text-muted-foreground sm:text-xl text-lg font-[family-name:var(--font-geist-sans)]">
          Welcome to the queue! Here, you can get help during office hours without needing to be physically present. Join the queue to reserve your spot in office hours.
        </p>
      </div>
      <div className="flex gap-4">
      
    <Button variant={"outline"} className="font-semibold" onClick={handleClick}>Join the Queue</Button>
      </div>
    </main>
  )
}