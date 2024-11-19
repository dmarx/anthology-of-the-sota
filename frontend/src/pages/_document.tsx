// frontend/src/pages/_document.tsx
import { Html, Head, Main, NextScript } from 'next/document';

export default function Document() {
  return (
    <Html lang="en">
      <Head />
      <body className="min-h-screen bg-gray-50">
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}
