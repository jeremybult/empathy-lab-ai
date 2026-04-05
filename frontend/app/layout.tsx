import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Empathy Lab AI',
  description: 'AI-powered persona chatbots for psychology education and empathy development.'
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
