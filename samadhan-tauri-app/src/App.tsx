import { useState } from "react";
import reactLogo from "./assets/react.svg";
import { invoke } from "@tauri-apps/api/core";

function App() {
  const [greetMsg, setGreetMsg] = useState("");
  const [name, setName] = useState("");

  async function greet() {
    setGreetMsg(await invoke("greet", { name }));
  }

  return (
    <main className="container mx-auto px-4 py-16">
      <h1 className="text-4xl font-bold text-center mb-8">
        Welcome to Tauri + React + Tailwind
      </h1>

      <div className="flex justify-center items-center gap-8 mb-8">
        <a href="https://vitejs.dev" target="_blank" className="hover:scale-110 transition-transform">
          <img src="/vite.svg" className="h-24" alt="Vite logo" />
        </a>
        <a href="https://tauri.app" target="_blank" className="hover:scale-110 transition-transform">
          <img src="/tauri.svg" className="h-24" alt="Tauri logo" />
        </a>
        <a href="https://reactjs.org" target="_blank" className="hover:scale-110 transition-transform">
          <img src={reactLogo} className="h-24" alt="React logo" />
        </a>
      </div>
      
      <p className="text-center text-lg mb-8">
        Click on the Tauri, Vite, and React logos to learn more
      </p>

      <form
        className="flex justify-center gap-4 mb-8"
        onSubmit={(e) => {
          e.preventDefault();
          greet();
        }}
      >
        <input
          id="greet-input"
          onChange={(e) => setName(e.currentTarget.value)}
          placeholder="Enter a name..."
          className="px-4 py-2 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-colors"
        />
        <button 
          type="submit"
          className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
        >
          Greet
        </button>
      </form>

      {greetMsg && (
        <p className="text-center text-xl">{greetMsg}</p>
      )}
    </main>
  );
}

export default App;
