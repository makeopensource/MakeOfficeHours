'use client'

import { AnimatePresence, motion } from "framer-motion";
import { X } from "lucide-react";
import React from "react";
import { Button } from "../ui/button";
import { on } from "events";

interface AnimatedModalProps{
    header:string,
    description:string,
    subDescription?:string,
    isOpen:boolean,
    onClose:()=>void
    onLeave:()=>void
}

export const AnimatedModal : React.FC<AnimatedModalProps> = ({header,description,subDescription,isOpen, onClose, onLeave}) => {
    return(
        <AnimatePresence>
            {isOpen &&(
                <motion.div
                    initial = {{opacity: 0}}
                    animate = {{opacity: 1}}
                    exit = {{opacity: 0}}
                    onClick={onClose}
                    className="bg-slate-900/20 backdrop-blur p-8 fixed inset-0 z-50 grid place-items-center overflow-y-scroll cursor-pointer"
                >
                    <motion.div
                        initial={{scale:0}}
                        animate={{scale:1}}
                        exit={{scale:0}}
                        onClick={(e) => e.stopPropagation()}
                        className="dark:bg-zinc-900 bg-zinc-100 rounded-lg sm:w-[25rem] max-w-lg shadow-xl cursor-default relative overflow-hidden"
                    >
                        <div className="flex flex-col">
                            <div className="flex items-center justify-between px-5 py-4">
                                <h1 className="text-lg font-semibold">{header}</h1>
                                <button onClick={onClose}>
                                    <X className="cursor-pointer dark:text-zinc-700 dark:hover:text-zinc-200 hover:text-zinc-900 text-zinc-400"/>
                                </button>
                            </div>
                            <div className="w-full border-[0.1px] dark:border-zinc-700 border-zinc-300"/>
                            <div className="flex flex-col px-5 py-4 gap-1">
                                <p className="text-sm text-muted-foreground font-semibold">{description}</p>
                                <p className="text-sm text-muted-foreground font-semibold">{subDescription}</p>
                            </div>
                            <div className="w-full border-[0.1px] dark:border-zinc-700 border-zinc-300"/>
                            <div className="flex justify-center py-4 px-5 gap-3">
                                <Button variant={"primary"} size={"default"} className="w-1/2 font-semibold" onClick={onClose}>
                                    Cancel
                                </Button>
                                <Button variant={"destructive"} size={"default"} className="w-1/2 font-semibold" onClick={onLeave}>
                                    Leave
                                </Button>
                            </div>
                        </div>

                    </motion.div>
                </motion.div>
            )}
        </AnimatePresence>
    )
}