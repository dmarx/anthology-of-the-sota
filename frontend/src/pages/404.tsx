import Link from 'next/link'

export default function Custom404() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full p-6">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-red-600 mb-4">404</h1>
          <p className="text-xl text-gray-600 mb-8">Page Not Found</p>
          <Link 
            href="/"
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          >
            Return Home
          </Link>
        </div>
      </div>
    </div>
  );
}
