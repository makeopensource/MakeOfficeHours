'use client'

import { useTheme } from "next-themes"
import React from "react"
import { Button } from "../ui/button";
import { MoonIcon, SunIcon } from "lucide-react";
import { Tooltip, TooltipProvider, TooltipContent, TooltipTrigger } from "../ui/tooltip";

export default function ModeToggle() {
    const { theme, setTheme } = useTheme();
    return (
      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger asChild>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            >
            <MoonIcon style={{width: "20px",height: "20px"}} className="h-[1.2rem] w-[1.2rem] text-neutral-800 dark:hidden dark:text-neutral-200" />
            <SunIcon style={{width: "20px",height: "20px"}} className="hidden h-[1.2rem] w-[1.2rem] text-neutral-800 dark:block dark:text-neutral-200" />
          </Button>
          </TooltipTrigger>
          <TooltipContent className="font-semibold">Change Theme</TooltipContent>
        </Tooltip>
      </TooltipProvider>
    )
}