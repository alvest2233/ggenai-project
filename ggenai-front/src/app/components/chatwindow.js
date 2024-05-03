import { useState, useRef } from 'react';
import dynamic from 'next/dynamic';
import ReactWebSocket from 'react-websocket';

// Dynamic imports for components without server-side rendering
const ChatMessage = dynamic(() => import("./chatmessage.js"), { ssr: false });
const SiteMessage = dynamic(() => import("./sitemessage.js"), { ssr: false });

export default function ChatWindow() {
  // State to store messages
  const [messages, setMessages] = useState([
    { message: "Hello World", didUserSend: false, type: 'text' },
    { message: "Hello World", didUserSend: true, type: 'text' },
    { message: "Here's your site!", didUserSend: false, sourceCode: `<html><head></head><body><h1>Hello World</h1></body></html>`, type: 'site' }
  ]);

  // WebSocket instance
  const [ws, setWs] = useState(null);

  // Reference for the message input
  const inputRef = useRef();

  // Function to add a new message to the state
  const addMessage = (message, didUserSend, sourceCode = null, type) => {
    setMessages([...messages, { message, didUserSend, sourceCode, type }]);
  };

  // Function to handle incoming WebSocket data
  const handleData = (data) => {
    let result = JSON.parse(data);
    addMessage(result.message, false);
  };

  // Function to send a message to the WebSocket server
  const sendMessage = (message) => {
    ws.send(JSON.stringify({ route: 'chat-user', message }));
  };

  // Function to handle sending a message when the 'Enter' key is pressed
  const handleQuery = () => {
    const message = inputRef.current.value;
    addMessage(message, true);
    sendMessage(message);
    inputRef.current.value = "";
  };

  return (
    <>
      <ReactWebSocket
        url='ws://localhost:8765'
        onMessage={handleData}
        onOpen={() => console.log('WebSocket Connected')}
        onClose={() => console.log('WebSocket Disconnected')}
        ref={(websocket) => { setWs(websocket); }}
      />
      <div className="flex-1 p:2 sm:p-6 justify-between flex flex-col h-screen">
        {/* Header */}
        <div className="flex sm:items-center justify-between py-3 border-b-2 border-gray-200">
          {/* ... header content ... */}
        </div>
        {/* Messages container */}
        <div id="messages" className="flex flex-col space-y-4 p-3 overflow-y-auto scrollbar-thumb-blue scrollbar-thumb-rounded scrollbar-track-blue-lighter scrollbar-w-2 scrolling-touch">
          {messages.map((contents, index) => (
            contents.type === 'text'
              ? <ChatMessage key={index} message={contents.message} didUserSend={contents.didUserSend} />
              : <>
                  {contents.message && <ChatMessage key={index} message={contents.message} didUserSend={contents.didUserSend} />}
                  <SiteMessage key={index} sourceCode={contents.sourceCode} />
                </>
          ))}
        </div>
        {/* Input container */}
        <div className="border-t-2 border-gray-200 px-4 pt-4 mb-2 sm:mb-0">
          <div className="relative flex">
            <input type="text" placeholder="Write your message!" className="w-full focus:outline-none focus:placeholder-gray-400 text-gray-600 placeholder-gray-600 pl-4 pr-24 bg-gray-200 rounded-md py-3" ref={inputRef} 
              onKeyDown={event => {
                if (event.key === 'Enter') {
                  handleQuery();
                  event.preventDefault(); // Prevents the addition of a new line in the input after pressing 'Enter'
                }
              }}/>
            <button type="button" className="inline-flex items-center justify-center rounded-lg px-4 py-3 transition duration-500 ease-in-out text-white bg-blue-500 hover:bg-blue-400 focus:outline-none" onClick={handleQuery}>
              <span className="font-bold">Send</span>
              {/* ... send icon ... */}
            </button>
          </div>
        </div>
      </div>
    </>
  );
}