import { Routes, Route } from 'react-router-dom'
import ChatPage from './pages/ChatPage'
import ClassifyPage from './pages/ClassifyPage'
import HomePage from './pages/HomePage'
import Navbar from './components/layout/Navbar'

export default function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-1">
        <Routes>
          <Route path="/"         element={<HomePage />} />
          <Route path="/chat"     element={<ChatPage />} />
          <Route path="/classify" element={<ClassifyPage />} />
        </Routes>
      </main>
    </div>
  )
}
