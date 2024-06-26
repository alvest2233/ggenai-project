"use client"
import Image from "next/image";
import dynamic from 'next/dynamic';

const ChatWindow = dynamic(() => import("./components/chatwindow"), { ssr: false });
// import ChatWindow from './components/chatwindow';
export default function Home() {
  return (
    <div className="flex flex-col h-screen">
      <header className="bg-gray-800 p-4">
        <div className="container mx-auto flex items-center">
          <img src="https://www.w3schools.com/w3images/avatar2.png" alt="Logo" className="h-8 mr-2" />
          <span className="text-white font-semibold text-lg">Ai Wireframer App!</span>
        </div>
      </header>
      <div className="flex-1 bg-gray-100 flex ">
        <div className="bg-white rounded-lg shadow-md p-6 ">
          <ChatWindow />
        </div>
      </div>
    </div>
  );
}
