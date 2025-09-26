'use client'

import { cn } from '@/lib/utils'
import { div } from 'motion/react-client'
import React, { FC, ReactNode } from 'react'

interface ShinyTextProps {
  children: ReactNode
  className?: string
}

export const ShinyText: FC<ShinyTextProps> = ({ children, className }) => {
  return (
    <div className="text-center">
      <h1 className={cn("bg-gradient-to-r from-slate-600 via-gray-500 to-slate-300 bg-clip-text text-transparent font-bold text-4xl sm:text-6xl", className)}>
        {children}
      </h1>
    </div>
  )
}
