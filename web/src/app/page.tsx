import { type Metadata } from 'next'

export const metadata: Metadata = {
  title: 'ML Recommendations',
  description: 'Machine Learning Training Recommendations'
}

export default function Home() {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">
        Machine Learning Recommendations (React Version)
      </h1>
      <p>React migration in progress...</p>
    </div>
  )
}
