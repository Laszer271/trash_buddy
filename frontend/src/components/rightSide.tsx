"use client";
import React, { useEffect, useState } from "react";
import CircularProgress from "@mui/material/CircularProgress";

type Props = {
  isLoading: boolean;
  answer: any;
};

const RightSide = ({ isLoading, answer }: Props) => {
  const [screenWidth, setScreenWidth] = useState(0);
  // answer = ["asdsadasdasd", "sadsadasdsad ", "asdasdsad"];
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
    <div className="flex flex-col items-center md:h-screen  w-[100vw] md:w-1/2 p-16">
      {screenWidth > 768 && (
        <p className="font-bold text-2xl text-center text-green-600">
          TrashBuddy
        </p>
      )}

      {/* {isLoading ? (
        <div className="flex items-center justify-center h-full">
          <CircularProgress />
        </div>
      ) : ( */}
      <div className="bg-gray-100 rounded-xl  w-[90vw] md:w-full  md:max-w-[600px] p-10 text-gray-600 md:mt-12 pb-20">
        <p className="font-bold text-center mb-6">Instructions</p>
        {answer &&
          answer.length > 0 &&
          answer.map((item: any, index: number) => (
            <p
              key={index}
              className="max-w-full overflow-hidden whitespace-normal break-words"
            >
              {item}
              <br />
            </p>
          ))}
      </div>
    </div>
  );
};

export default RightSide;
