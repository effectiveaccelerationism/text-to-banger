"use client";

import { useChat } from "ai/react";
import Image from "next/image";
import ThemeButton from "./ThemeButton";

export default function BangerModal() {
  const {
    messages,
    input: tweetIdea,
    handleInputChange,
    handleSubmit,
    isLoading,
  } = useChat({
    api: "/api/banger",
    initialMessages: [
      {
        content:
          "Sorry babe I can't listening how was your day ever again. I lose my edge context-switching to your toxic work environment",
        role: "user",
        id: "ISgO141",
      },
      {
        id: "XEAnGmj",
        content:
          "I just saw someone walking around with a sign that said 'I'm an undefined variable' and I couldn't help but think, same.",
        role: "system",
      },
      {
        content: "I dont know mannn",
        role: "user",
        id: "TftCoI2",
      },
      {
        id: "dnE9T9I",
        content:
          "Just found out my ex was an alien the whole time. Talk about out of this world!",
        role: "assistant",
      },
      {
        content: "thanks broter",
        role: "user",
        id: "JSK2xq1",
      },
      {
        id: "BgeGxWj",
        content:
          "Ducks are so weird. I mean, have you ever seen one wearing pants?",
        role: "assistant",
      },
      {
        content: "hehehehehehehehehe",
        role: "user",
        id: "5KyZadz",
      },
      {
        id: "3WrgVR6",
        content:
          "My therapist just told me I have an unhealthy obsession with the Oxford comma. I think it's time to take a break from our sessions.",
        role: "assistant",
      },
    ],
  });

  return (
    <div className="text-center text-black dark:text-white">
      <ThemeButton />
      <header className="min-h-screen flex flex-col justify-center light:bg-white dark:bg-black">
        <div className="flex justify-center w-full">
          <h1 className="font-mono mb-6 text-5xl font-bold dark:text-white">
            text-to-banger
          </h1>
        </div>
        <div className="flex flex-col items-center justify-center mx-5 text-lg">
          <form
            onSubmit={handleSubmit}
            className="bg-gradient-to-br bg-transparent border border-black dark:border-white rounded-sm px-2.5 pt-2 pb-3 w-full max-w-[700px] flex flex-col shadow-md"
          >
            <textarea
              id="tweetIdea"
              value={tweetIdea}
              onChange={handleInputChange}
              placeholder="What's happening?"
              rows={4}
              className="border-none p-2 resize-none outline-none font-mono placeholder-[#757575] bg-transparent"
            />
            <button
              className="border border-black dark:border-white p-1 text-center font-mono rounded-sm cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed"
              type="submit"
              disabled={isLoading || !tweetIdea}
            >
              {isLoading ? (
                <Image
                  src="spinner.svg"
                  className="animate-spin mx-auto"
                  alt="spinner"
                  width={20}
                  height={20}
                />
              ) : (
                <p>Generate Banger Tweet</p>
              )}
            </button>
          </form>
          <div className="m-auto pt-5 mt-4 rounded-lg max-w-[700px] h-96 overflow-y-auto overflow-x-hidden font-mono">
            {messages.map((m, index) => (
              <div
                key={m.id}
                className={`pl-4 pr-1 text-left ${
                  index % 2 === 0 ? "mb-3" : "mb-9"
                }`}
              >
                <strong>{m.role === "user" ? "Prompt" : "Banger"}:</strong>{" "}
                {m.content}
              </div>
            ))}
          </div>
        </div>
      </header>
    </div>
  );
}
