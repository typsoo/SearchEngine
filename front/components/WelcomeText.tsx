"use client";

import { useEffect, useState } from "react";

export default function WelcomeText() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setMounted(true), 50);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div
      className={`mb-8 text-center transition-all duration-1000 ease-out transform ${
        mounted ? "translate-y-0 opacity-100" : "translate-y-8 opacity-0"
      }`}
    >
      <h1 className="mb-4 text-4xl font-extrabold tracking-tight text-slate-800 md:text-5xl drop-shadow-sm">
        Just worst Google
      </h1>
      <p className="mx-auto max-w-xl text-lg text-slate-700 drop-shadow-sm">
        Enter your query below to explore database using custom castom and
        library algorithms.
      </p>
    </div>
  );
}
