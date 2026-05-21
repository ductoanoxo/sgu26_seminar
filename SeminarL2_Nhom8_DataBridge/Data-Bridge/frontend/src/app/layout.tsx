import type { Metadata } from 'next';
import { Schibsted_Grotesk, Inter, Noto_Sans, Fustat } from 'next/font/google';
import './globals.css';

const schibsted = Schibsted_Grotesk({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700'],
  variable: '--font-schibsted',
});

const inter = Inter({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700'],
  variable: '--font-inter',
});

const notoSans = Noto_Sans({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700'],
  variable: '--font-noto',
});

const fustat = Fustat({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700'],
  variable: '--font-fustat',
});

export const metadata: Metadata = {
  title: 'NL2SQL Dashboard — Natural Language to SQL',
  description:
    'Convert natural language questions into SQL queries, execute them on PostgreSQL, and visualize results with interactive charts.',
};

import { ToastProvider } from '@/context/ToastContext';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${schibsted.variable} ${inter.variable} ${notoSans.variable} ${fustat.variable}`}>
        <ToastProvider>
          {children}
        </ToastProvider>
      </body>
    </html>
  );
}
