"use client";

import { useEffect, useState } from "react";
import { useTheme } from "next-themes";

const ThemeButton = () => {
  const { resolvedTheme, setTheme } = useTheme();

  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return null;
  }

  return (
    <button
      className="text-white p-2 rounded-full fixed top-5 right-5 w-10 h-10 text-lg shadow-md hover:bg-[#888] transition"
      onClick={() => setTheme(resolvedTheme === "dark" ? "light" : "dark")}
    >
      {resolvedTheme === "dark" ? "🌙" : "☀️"}
    </button>
  );
};

export default ThemeButton;
