"use client";

// import Image from "next/image";
import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import axios from "axios";

import compress from 'compress-base64'

type Props = {
  isLoading: boolean;
  setIsLoading: (value: boolean) => void;
  answer: any;
  setAnswer: (value: any) => void;
};

const LeftSide = ({ isLoading, setIsLoading, answer, setAnswer }: Props) => {
  const [trash, setTrash] = useState<string>();

  const handleImageUpload = async (base64String: string) => {
    try {
      await axios
        .post("https://server-a4qtbsflp-laszer271s-projects.vercel.app/chat/", {
          // .post("http://127.0.0.1:8000/chat/", {
          base64: base64String, //https://server-fi8pef6pv-laszer271s-projects.vercel.app/chat
          timeout: 30000, // Ustaw timeout na 10 sekund (10000 milisekund)
          withCredentials: true,
        })
        .then((response) => {
          console.log("Response:", response.data.message);

          setAnswer(response.data.message);
          setIsLoading(false);
        })
        .catch((error) => {
          console.log("Error:", error);
          setIsLoading(false);
        })
        .finally(() => {});
    } catch (err) {
      console.log("gowno");
    }
  };

  const onDrop = useCallback((acceptedFiles: File[]) => {
    acceptedFiles.forEach((file: File) => {
      setIsLoading(true); // Set loading state at the beginning of the process
  
      const reader = new FileReader();
      reader.onload = event => {
        const result = event.target?.result;
        if (typeof result === "string") { // Ensure result is treated as a string
          compress(result, {
            width: 512, // Desired width
            height: 512, // Desired height
            type: 'image/png', // Output type
            max: 200, // Maximum output file size in KB
            min: 20,  // Minimum output file size in KB
            quality: 0.8, // Compression quality
          }).then(compressedResult => {
            console.log(compressedResult); // You get a base64 string back
            setTrash(compressedResult.base64); // Save base64 string for display or further use
            handleImageUpload(compressedResult.base64); // Upload the compressed image
            setIsLoading(false); // Reset loading state after processing
          }).catch(error => {
            console.error("Compression Error:", error);
            setIsLoading(false); // Ensure to reset loading state on error
          });
        } else {
          console.error("Expected a string from FileReader but received a different type.");
          setIsLoading(false);
        }
      };
      reader.onerror = () => {
        console.error("FileReader Error");
        setIsLoading(false);
      };
      reader.readAsDataURL(file); // Read the file as Data URL to handle images
    });
  }, [setIsLoading, handleImageUpload, setTrash]);
  
  
  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: { "image/*": [] },
  });

  return (
    <div className="flex flex-col justify-between md:bg-gray-100 h-[400px] md:h-[100%] w-[100vw] md:w-[50%]">
      <div
        className={`hover:cursor-pointer rounded-3xl md:w-[20%] w-[70%]  shadow-custom mx-auto text-center p-5 ${
          isLoading ? "pointer-events-none opacity-50" : ""
        }`}
        {...getRootProps()}
      >
        <input {...getInputProps()} className="" />
        {/* <p className="font-serif text-lg ">Wrzuć zdjęcie śmieci</p> */}
        {/* <Image alt="Drop" src="/drop.png" height="500" width="500"></Image> */}
        <button
          onClick={() => {}}
          className="bg-[#2c9f56] text-white mt-12 text-wrap py-2 px-4  border-0 rounded-md"
        >
          Upload a photo
        </button>
      </div>

      <div className="mx-auto mb-[2%] md:mb-[20%]">
        {trash && (
          <div>
            <img
              src={`data:image/png;base64,${trash}`}
              alt="Uploaded"
              style={{
                margin: "auto",
                maxWidth: "90%",
                maxHeight: "300px", // Ustaw maksymalną wysokość obrazu
                borderRadius: "14px", // Zaokrąglenie rogów
              }}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default LeftSide;
