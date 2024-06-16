"use client";
import Navbar from "@/components/common/Navbar";
import LeftSide from "@/components/leftSide";
import RightSide from "@/components/rightSide";
import { useEffect, useState } from "react";

export default function Home() {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [answer, setAnswer] = useState<any>();

  const [screenWidth, setScreenWidth] = useState(0);

  useEffect(() => {
    const handleResize = () => {
      setScreenWidth(window.innerWidth);
    };

    // Initial set of screenWidth
    setScreenWidth(window.innerWidth);

    // Add event listener for window resize
    window.addEventListener("resize", handleResize);

    // Cleanup function to remove event listener
    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  return (
    <div className="flex  flex-col md:flex-row   h-[100vh]">
      {screenWidth < 768 && <Navbar />}
      <LeftSide
        isLoading={isLoading}
        setIsLoading={setIsLoading}
        answer={answer}
        setAnswer={setAnswer}
      />
      <RightSide isLoading={isLoading} answer={answer} />
    </div>
  );
}
