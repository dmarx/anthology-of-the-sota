// frontend/src/pages/_app.tsx
import '@/styles/globals.css'
import type { AppProps } from 'next/app'

export default function App({ Component, pageProps }: AppProps) {
  // Add error boundary and debugging
  console.log('Rendering App with props:', { pageProps });
  
  return (
    <>
      <Component {...pageProps} />
    </>
  );
}
