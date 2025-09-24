"use client"

import { Bell, Search, User } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ThemeToggle } from "@/components/ui/theme-toggle"
import { motion } from "framer-motion"

interface NavbarProps {
  className?: string
}

export function Navbar({ className }: NavbarProps) {
  return (
    <motion.header
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className={`sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 ${className}`}
    >
      <div className="flex h-16 items-center justify-between px-6">
        {/* Search */}
        <div className="flex flex-1 items-center gap-4 max-w-md">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              placeholder="Search stocks, symbols..."
              className="pl-10 h-9"
            />
          </div>
        </div>

        {/* Right side actions */}
        <div className="flex items-center gap-3">
          <Button className="h-9 w-9 bg-transparent hover:bg-gray-100">
            <Bell className="h-4 w-4" />
          </Button>
          
          <ThemeToggle />
          
          <Button className="h-9 w-9 bg-transparent hover:bg-gray-100">
            <User className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </motion.header>
  )
}