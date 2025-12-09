import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Taj Chat - Create Videos Without Limits | AI Video Creator',
  description: 'Turn any idea into videos. Ads, explainers, stories, YouTube Shorts, TikToks — our AI creates publish-ready videos in minutes. 10 specialized AI agents working together.',
  keywords: 'AI video generator, video creator, TikTok maker, YouTube Shorts, Instagram Reels, AI music, viral videos',
  authors: [{ name: 'Taj Chat' }],
  openGraph: {
    title: 'Taj Chat - Create Videos Without Limits',
    description: 'Turn any idea into videos with AI. Create stunning content in minutes.',
    type: 'website',
    locale: 'en_US',
    siteName: 'Taj Chat',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Taj Chat - Create Videos Without Limits',
    description: 'Turn any idea into videos with AI. Create stunning content in minutes.',
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="scroll-smooth">
      <head>
        <link rel="icon" href="/favicon.ico" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
      </head>
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
