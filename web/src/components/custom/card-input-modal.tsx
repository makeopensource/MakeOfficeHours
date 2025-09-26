'use client'

import { AnimatePresence, motion } from "framer-motion";
import { X } from "lucide-react";
import React, { useState } from "react";
import { Button } from "../ui/button";
import { QueueForm } from "../queue/queue-form";

interface CardInputModalProps {
  header: string;
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (formData: any) => void;
}

export const CardInputModal: React.FC<CardInputModalProps> = ({
  header,
  isOpen,
  onClose,
  onSubmit
}) => {

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
          className="bg-slate-900/20 backdrop-blur p-8 fixed inset-0 z-50 grid place-items-center overflow-y-scroll cursor-pointer"
        >
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            exit={{ scale: 0 }}
            onClick={(e) => e.stopPropagation()}
            className="dark:bg-zinc-900 bg-zinc-100 rounded-lg w-[90%] max-w-3xl shadow-xl cursor-default relative overflow-hidden"
          >
            <div className="flex flex-col">
              <div className="flex items-center justify-between px-5 py-4">
                <h1 className="text-lg font-semibold">{header}</h1>
                <button onClick={onClose}>
                  <X className="cursor-pointer dark:text-zinc-700 dark:hover:text-zinc-200 hover:text-zinc-900 text-zinc-400" />
                </button>
              </div>
              <div className="px-5 py-4">
                <QueueForm 
                  onSubmit={onSubmit}
                  role="student"
                  onClose={onClose}
                />
              </div>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};
