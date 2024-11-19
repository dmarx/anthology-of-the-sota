export default function Custom500() {
  return (
    <div className="min-h-screen p-4">
      <div className="max-w-7xl mx-auto p-4 bg-red-50 border border-red-200 rounded">
        <h1 className="text-red-800 text-xl font-bold">500 - Server Error</h1>
        <p className="text-red-600">An unexpected error occurred. Please try again later.</p>
      </div>
    </div>
  )
}
